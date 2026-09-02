output "cloud_run_uri" {
  description = "The URL of the deployed Cloud Run service"
  value       = google_cloud_run_v2_service.app_service.uri
}

output "cloud_sql_connection_name" {
  description = "Cloud SQL connection name"
  value       = google_sql_database_instance.postgres.connection_name
}

output "storage_bucket_name" {
  description = "Cloud Storage bucket for attachments"
  value       = google_storage_bucket.attachments.name
}

output "service_account_email" {
  description = "Service Account email"
  value       = google_service_account.app_sa.email
}
