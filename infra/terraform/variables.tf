variable "resource_group_name" {
  description = "Azure resource group name for the lab."
  type        = string
  default     = "rg-open-data-ai-lab4"
}

variable "location" {
  description = "Azure region."
  type        = string
  default     = "westeurope"
}

variable "project_prefix" {
  description = "Prefix for Azure resources."
  type        = string
  default     = "open-data-ai"
}

variable "admin_username" {
  description = "Linux VM administrator username."
  type        = string
  default     = "azureuser"
}

variable "ssh_public_key_path" {
  description = "Path to SSH public key in Azure Cloud Shell."
  type        = string
  default     = "~/.ssh/id_rsa.pub"
}

variable "vm_size" {
  description = "Linux VM size."
  type        = string
  default     = "Standard_B1s"
}

variable "web_port" {
  description = "Public web port opened in the Network Security Group."
  type        = number
  default     = 8000
}

variable "repo_url" {
  description = "Git repository cloned by cloud-init."
  type        = string
  default     = "https://github.com/Djullaii/open-data-ai-analytics.git"
}

variable "repo_branch" {
  description = "Repository branch used by cloud-init."
  type        = string
  default     = "main"
}

