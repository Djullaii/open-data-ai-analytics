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

output "ssh_command" {
  description = "SSH command for checking the VM."
  value       = "ssh ${var.admin_username}@${azurerm_public_ip.lab.ip_address}"
}

