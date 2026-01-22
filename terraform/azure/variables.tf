variable "resource_group_name" {
  description = "Name of the resource group"
  type        = string
  default     = "chatbot-rg"
}

variable "location" {
  description = "Azure region"
  type        = string
  default     = "eastus"
}

variable "redis_capacity" {
  description = "Redis cache capacity"
  type        = number
  default     = 0
}

variable "redis_family" {
  description = "Redis cache family"
  type        = string
  default     = "C"
}

variable "redis_sku_name" {
  description = "Redis cache SKU name"
  type        = string
  default     = "Basic"
}

variable "acr_name" {
  description = "Azure Container Registry name"
  type        = string
  default     = "chatbotacr"
}

variable "app_service_name" {
  description = "App Service name"
  type        = string
  default     = "chatbot-app"
}

variable "app_service_sku" {
  description = "App Service SKU"
  type        = string
  default     = "B1"
}

variable "key_vault_name" {
  description = "Key Vault name"
  type        = string
  default     = "chatbot-kv"
}

variable "openai_api_key" {
  description = "OpenAI API key"
  type        = string
  sensitive   = true
}
