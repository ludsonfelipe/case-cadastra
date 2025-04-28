resource "google_sql_database_instance" "instance" {
    name             = var.instance_cloud_sql
    database_version = "POSTGRES_15"
    region           = var.project_region
    settings {
        tier = "db-g1-small"

        disk_size = "20"
        database_flags {
          name = "cloudsql.logical_decoding"
          value = "on"
        }

        ip_configuration {

            authorized_networks {
                value = "0.0.0.0/0"
            }
        }
    }

    deletion_protection  = "false"
}

resource "google_sql_database" "db" {
    instance = google_sql_database_instance.instance.name
    name     = var.database_name
}

resource "google_sql_user" "user" {
    name = var.user
    instance = google_sql_database_instance.instance.name
    password = var.password
}