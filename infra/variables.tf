variable "project_name" {
  description = "Nom du projet, utilisé comme préfixe pour toutes les ressources Azure"
  type        = string
  default     = "pianops"
}

variable "environment" {
  description = "Nom de l'environnement (ex: prod, dev)"
  type        = string
  default     = "prod"
}

variable "location" {
  description = "Région Azure où déployer les ressources"
  type        = string
  default     = "swedencentral"
}

variable "tags" {
  description = "Tags communs appliqués à toutes les ressources"
  type        = map(string)
  default = {
    project    = "pianops"
    managed_by = "terraform"
  }
}
