output "app_service_url" {
  description = "App Service URL"
  value       = "https://${azurerm_linux_web_app.main.default_hostname}"
}

output "redis_hostname" {
  description = "Redis hostname"
  value       = azurerm_redis_cache.main.hostname
  sensitive   = true
}

output "container_registry_url" {
  description = "Container Registry URL"
  value       = azurerm_container_registry.main.login_server
}
