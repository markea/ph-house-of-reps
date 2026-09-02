terraform {
  required_version = ">= 1.5.0"
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 5.20"
    }
    random = {
      source  = "hashicorp/random"
      version = "~> 3.6"
    }
  }
}

provider "google" {
  project = var.project_id
  region  = var.region
}

# 1. Random Password for Database
resource "random_password" "db_password" {
  length  = 24
  special = false
}

# 2. Service Account for Cloud Run (Least Privilege)
resource "google_service_account" "app_sa" {
  account_id   = "${var.app_name}-sa"
  display_name = "HRep e-Request Service Account"
}

# 3. Cloud Storage for Requisition Attachments
resource "google_storage_bucket" "attachments" {
  name                        = "${var.project_id}-${var.app_name}-attachments"
  location                    = var.region
  uniform_bucket_level_access = true
  force_destroy               = false

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 1095 # 3 Years COA Retention Schedule
    }
  }
}

# Grant Cloud Run SA read/write to the bucket
resource "google_storage_bucket_iam_member" "storage_admin" {
  bucket = google_storage_bucket.attachments.name
  role   = "roles/storage.objectAdmin"
  member = "serviceAccount:${google_service_account.app_sa.email}"
}

# 4. Cloud SQL for PostgreSQL (Production HA)
resource "google_sql_database_instance" "postgres" {
  name             = "${var.app_name}-db-prod"
  database_version = "POSTGRES_15"
  region           = var.region

  settings {
    tier              = "db-custom-2-7680" # 2 vCPU, 7.5 GB RAM
    availability_type = "REGIONAL"         # High-availability Multi-Zone
    disk_size         = 50
    disk_type         = "PD_SSD"
    disk_autoresize   = true

    backup_configuration {
      enabled                        = true
      point_in_time_recovery_enabled = true
      start_time                     = "02:00"
    }

    insights_config {
      query_insights_enabled = true
    }

    ip_configuration {
      ipv4_enabled = true
      require_ssl  = true
    }
  }
  deletion_protection = true
}

resource "google_sql_database" "database" {
  name     = "erequests_db"
  instance = google_sql_database_instance.postgres.name
}

resource "google_sql_user" "users" {
  name     = "erequest_app"
  instance = google_sql_database_instance.postgres.name
  password = random_password.db_password.result
}

# Grant Cloud SQL Client role to SA
resource "google_project_iam_member" "sql_client" {
  project = var.project_id
  role    = "roles/cloudsql.client"
  member  = "serviceAccount:${google_service_account.app_sa.email}"
}

# 5. Secret Manager for DB Password
resource "google_secret_manager_secret" "db_secret" {
  secret_id = "${var.app_name}-db-password"

  replication {
    auto {}
  }
}

resource "google_secret_manager_secret_version" "db_secret_version" {
  secret      = google_secret_manager_secret.db_secret.id
  secret_data = random_password.db_password.result
}

# 6. Cloud Run Service
resource "google_cloud_run_v2_service" "app_service" {
  name     = var.app_name
  location = var.region
  ingress  = "INGRESS_TRAFFIC_INTERNAL_LOAD_BALANCER" # Restrict to IAP Load Balancer

  template {
    service_account = google_service_account.app_sa.email

    scaling {
      min_instance_count = 1 # 1 Warm instance for zero cold starts during session
      max_instance_count = 10
    }

    volumes {
      name = "cloudsql"
      cloud_sql_instance {
        instances = [google_sql_database_instance.postgres.connection_name]
      }
    }

    containers {
      image = var.container_image

      resources {
        limits = {
          cpu    = "2"
          memory = "2Gi"
        }
      }

      env {
        name  = "APP_ENV"
        value = "production"
      }
      env {
        name  = "AUTH_MODE"
        value = "iap"
      }
      env {
        name  = "STORAGE_TYPE"
        value = "gcs"
      }
      env {
        name  = "GCS_BUCKET_NAME"
        value = google_storage_bucket.attachments.name
      }
      env {
        name  = "DATABASE_URL"
        value = "postgresql+psycopg2://erequest_app:${random_password.db_password.result}@/erequests_db?host=/cloudsql/${google_sql_database_instance.postgres.connection_name}"
      }

      volume_mounts {
        name       = "cloudsql"
        mount_path = "/cloudsql"
      }

      startup_probe {
        http_get {
          path = "/healthz"
          port = 8080
        }
        initial_delay_seconds = 5
        period_seconds        = 5
        failure_threshold     = 3
      }

      liveness_probe {
        http_get {
          path = "/healthz"
          port = 8080
        }
        period_seconds = 10
      }
    }
  }

  depends_on = [
    google_sql_database.database,
    google_sql_user.users,
    google_storage_bucket.attachments
  ]
}
