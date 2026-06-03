output "resource_group_name" {
  description = "Created resource group."
  value       = azurerm_resource_group.lab.name
}

output "public_ip" {
  description = "Public IP address of the Linux VM."
  value       = azurerm_public_ip.lab.ip_address
}

output "web_url" {
  description = "URL of the deployed web interface."
  value       = "http://${azurerm_public_ip.lab.ip_address}:${var.web_port}"
}

output "prometheus_url" {
  description = "URL of the Prometheus interface."
  value       = "http://${azurerm_public_ip.lab.ip_address}:${var.prometheus_port}"
}

output "grafana_url" {
  description = "URL of the Grafana interface."
  value       = "http://${azurerm_public_ip.lab.ip_address}:${var.grafana_port}"
}

output "gitops_app_url" {
  description = "URL of the GitOps-managed web application."
  value       = "http://${azurerm_public_ip.lab.ip_address}:${var.gitops_app_port}"
}

output "argocd_url" {
  description = "URL of the Argo CD interface."
  value       = "https://${azurerm_public_ip.lab.ip_address}:${var.argocd_port}"
}

output "ssh_command" {
  description = "SSH command for checking the VM."
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.lab.ip_address}"
}
