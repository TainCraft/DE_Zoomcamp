terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "4.51.0"
    }
  }
}

provider "google" {
  # Credentials only needs to be set if you do not have the GOOGLE_APPLICATION_CREDENTIALS set
  credentials = "C:\\data_engineering\\week _1\\2_docker_sql\\terrademo\\keys\\my-cred.json"
  project     = "adept-lodge-412310"
  region      = "us-central1"
}



resource "google_storage_bucket" "data-lake-bucket" {
  name     = "terra_bucket"
  location = "US"

  # Optional, but recommended settings:
  storage_class               = "STANDARD"
  uniform_bucket_level_access = true

  versioning {
    enabled = true
  }

  lifecycle_rule {
    action {
      type = "Delete"
    }
    condition {
      age = 30 // days
    }
  }

  force_destroy = true
}


resource "google_bigquery_dataset" "dataset" {
  dataset_id = "green_taxi_dataset"
  project    = "adept-lodge-412310"
  location   = "US"
}