---
title: "Getting Started with Terraform"
date: "2025-01-01"
summary: "A beginner's guide to Infrastructure as Code with Terraform."
tags:
  - Terraform
  - IaC
  - DevOps
---

Terraform lets you define infrastructure as code. Here's how to get started.

## Installation

```bash
brew install terraform
```

## Your First Configuration

Create a `main.tf`:

```hcl
provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "example" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
}
```

## Commands

```bash
terraform init
terraform plan
terraform apply
```

That's it. Infrastructure as Code in 3 steps.
