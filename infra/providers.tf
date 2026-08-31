terraform {
  required_version = ">= 1.15"

  required_providers {
    azurerm = {
      source  = "hashicorp/azurerm"
      version = ">= 4.0"

    }

    random = {
      source  = "hashicorp/random"
      version = ">= 3.0"
    }
  }

  backend "azurerm" {
    subscription_id      = "67b5662b-ae04-4d03-a5ac-b0cd67a87c2e"
    resource_group_name  = "rg-pianops-tfstate"
    storage_account_name = "stpianopstfstate2026"
    container_name       = "tfstate"
    key                  = "pianops.tfstate"
  }
}

provider "azurerm" {
  subscription_id = "67b5662b-ae04-4d03-a5ac-b0cd67a87c2e"
  features {}
}
