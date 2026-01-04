---
title: "Terraform AWS HIPAA Module"
date: "2024-06-15"
summary: "Open-source Terraform module for deploying HIPAA-compliant infrastructure on AWS."
tags:
  - Terraform
  - AWS
  - HIPAA
  - Security
---

## The Problem

Healthcare organizations face a significant barrier when moving to the cloud: HIPAA compliance.

## The Solution

I created `terraform-aws-hipaa`, a Terraform module that deploys a fully HIPAA-compliant AWS infrastructure in under an hour.

### Key Features

- VPC with public/private subnet architecture
- AWS WAF with OWASP Top 10 rules
- CloudTrail logging to encrypted S3
- KMS encryption for all data stores

## Usage

```hcl
module "hipaa_infrastructure" {
  source  = "ummahrican/hipaa/aws"
  version = "2.1.0"

  environment  = "production"
  project_name = "my-health-app"
}
```

## Impact

- 850+ GitHub stars
- 15,000+ downloads
- 50+ healthcare organizations using in production
