terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.42.1"
    }
  }
}

provider "google" {
  project = var.project
}

# Mlflow server
resource "google_compute_instance" "default" {
  name         = "mlflow-server-tf"
  machine_type = "e2-medium"
  zone         = "us-central1-a"

  tags = ["mlflow", "models"]

  boot_disk {
    initialize_params {
      image = "debian-cloud/debian-11"
      labels = {
        my_label = "value"
      }
    }
  }

  network_interface {
    network = "default"

    access_config {
      // Ephemeral public IP
    }
  }

  service_account {
    # Google recommends custom service accounts that have cloud-platform scope and permissions granted via IAM Roles.
    email  = "tf-deployer@fveloso-latam.iam.gserviceaccount.com" # setting SA as var
    scopes = ["cloud-platform"]
  }
}

# create source code repositories
resource "google_sourcerepo_repository" "flight_repo" {
  name = "flight_prediction_tf"
}

data "google_artifact_registry_repository" "flight_model" {
  location      = "us-central1"
  repository_id = "flight-predict-tf"
}

# triger cloud build 
resource "google_cloudbuild_trigger" "flight-pred-build" {

  name = "flight-pred-build-tf"
  location = "us-central1"
  # service_account = "tf-deployer@fveloso-latam.iam.gserviceaccount.com" # setting SA as var
  trigger_template {
    branch_name = "develop"
    repo_name   = google_sourcerepo_repository.flight_repo.name
  }
  # dependiendo de las condiciones es factible crear las instrucciones via tf, en este caso depende del dev el ciclo de integracion
  
  substitutions = {
    _PROJECT_ID = var.project
    _SERVICE_NAME = "model-flight" # set as a var
    _MODEL_NAME = "flight-predict" # set as a var
  }
  filename = "cloudbuild.yaml"
  tags = ["dev", "model"]
}

# el crear la imagen, gatilla automaticamente el job de cloud run, si la necesidad de la organizacion es controlar el pipeline por completo, se podría orquestar mediante workflows/composer
  

resource "google_sourcerepo_repository" "flight_api_repo" {
  name = "flight_prediction_api_tf"
}

data "google_artifact_registry_repository" "flight-api" {
  location      = "us-central1"
repository_id = "flight-predict-api-tf"
}

# triger cloud build 
resource "google_cloudbuild_trigger" "flight-pred-api" {

  name = "flight-pred-api-tf"
  location = "us-central1"
  
  # service_account = "tf-deployer@fveloso-latam.iam.gserviceaccount.com" # setting SA as var
  trigger_template {
    branch_name = "develop"
    repo_name   = google_sourcerepo_repository.flight_api_repo.name
  }
  # dependiendo de las condiciones es factible crear las instrucciones via tf, en este caso depende del dev el ciclo de integracion
  
  substitutions = {
    _PROJECT_ID = var.project
    _SERVICE_NAME = "model-flight-api" # set as a var
    _MODEL_NAME = "flight-predict-api" # set as a var
  }
  filename = "cloudbuild.yaml"
  tags = ["dev", "api"]
}

