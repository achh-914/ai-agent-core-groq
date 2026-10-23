terraform {
  required_version = ">= 1.0.0"
  required_providers {
    local = {
      source  = "hashicorp/local"
      version = "2.4.0"
    }
  }
}

provider "local" {}

resource "local_file" "agent_config" {
  filename = "${path.module}/agent_env_setup.txt"
  content  = <<EOF
===========================================
AI Agent Core Infrastructure Setup
Model: Llama 3 (via Groq API)
Status: Provisioned successfully
===========================================
EOF
}
