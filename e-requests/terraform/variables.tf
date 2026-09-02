variable "project_id" {
  description = "The Google Cloud Project ID"
  type        = string
}

variable "region" {
  description = "Google Cloud region for resources"
  type        = string
  default     = "asia-southeast1" # Manila / Singapore
}

variable "environment" {
  description = "Deployment environment"
  type        = string
  default     = "production"
}

variable "app_name" {
  description = "Application name"
  type        = string
  default     = "hrep-erequests"
}

variable "iap_support_email" {
  description = "OAuth support email for Identity-Aware Proxy"
  type        = string
  default     = "it-admin@hrep.gov.ph"
}

variable "container_image" {
  description = "Container image URI in Artifact Registry"
  type        = string
  default     = "asia-southeast1-docker.pkg.dev/PROJECT_ID/hrep-repo/erequests-app:latest"
}
