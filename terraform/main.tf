provider "google" {
  credentials = file("./key/key.json")
  project     = var.project
  region      = var.region
}
provider "google-beta" {
  credentials = file("./key/key.json")
  project     = var.project
  region      = var.region
}

module "project-services" {
  source                      = "terraform-google-modules/project-factory/google//modules/project_services"
  version                     = "17.0.0"
  disable_services_on_destroy = false

  project_id  = var.project
  enable_apis = var.enable_apis

  activate_apis = [
    "serviceusage.googleapis.com",
    "cloudresourcemanager.googleapis.com",
    "cloudapis.googleapis.com",
    "sqladmin.googleapis.com",
    "iam.googleapis.com"
  ]
}

# Generate a random bucket id
resource "random_id" "bucket_id" {
  byte_length = 4
}

# # Create the buckets
# module "buckets" {
#   source = "./buckets"

#   bucket_name_database = "raw-database-${random_id.bucket_id.hex}"
#   location = "US"
# }

# Create the database
module "database" {

  source = "./cloudsql"
  project_region = var.region
  project_id = var.project

  user = "postgres"
  password = "123456"
  database_name = "cryptodb"
  instance_cloud_sql = "postgres"
  depends_on = [ module.project-services ]
}
