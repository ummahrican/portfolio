---
title: "Terraform AWS HIPAA Module"
faqs:
  - question: "What is a HIPAA-compliant AWS infrastructure?"
    answer: "HIPAA-compliant AWS infrastructure includes encrypted data storage, comprehensive audit logging, network segmentation, automated backups, and access controls that meet the technical safeguards required by the Health Insurance Portability and Accountability Act for protecting patient health information (PHI)."
  - question: "How long does it take to deploy HIPAA-compliant infrastructure on AWS?"
    answer: "Using the terraform-aws-hipaa module, you can deploy a fully HIPAA-compliant AWS infrastructure in under an hour. Without a pre-built module, manual setup typically takes 3-6 months."
  - question: "Is this Terraform module free to use?"
    answer: "Yes, terraform-aws-hipaa is open source under the MIT license, free for both commercial and personal use. You only pay for the AWS resources the module provisions."
  - question: "What AWS services does the HIPAA module configure?"
    answer: "The module configures VPC with public/private subnets, RDS with encryption and automated backups, S3 with versioning and MFA delete, CloudTrail for audit logging, GuardDuty for threat detection, Security Hub for compliance monitoring, KMS for encryption keys, and WAF for web application firewall rules."
description: "Open-source Terraform module for deploying HIPAA-compliant infrastructure on AWS. Used by 50+ healthcare organizations to accelerate compliant cloud adoption."
type: "Open Source"
year: "2024"
client: "Open Source Community"
link: "https://github.com/ummahrican/terraform-aws-hipaa"
github: "https://github.com/ummahrican/terraform-aws-hipaa"
tech:
  - Terraform
  - AWS
  - HIPAA
  - Security
  - Infrastructure as Code
# SEO enhancements
featured: true
# image: "/static/portfolio/terraform-hipaa-og.png"
---

## The Problem

Healthcare organizations face a significant barrier when moving to the cloud: HIPAA compliance. The Health Insurance Portability and Accountability Act requires specific technical safeguards that are complex to implement correctly:

- Encryption at rest and in transit
- Access logging and audit trails
- Network segmentation
- Automatic backups with retention policies
- Incident response capabilities

Most teams spend 3-6 months just getting the infrastructure compliant before they can deploy their first application.

## The Solution

I created `terraform-aws-hipaa`, a comprehensive Terraform module that deploys a fully HIPAA-compliant AWS infrastructure in under an hour. It codifies years of healthcare infrastructure experience into reusable, audited code.

### Key Features

**🔐 Security First**

- VPC with public/private subnet architecture
- AWS WAF with OWASP Top 10 rules
- GuardDuty threat detection enabled
- Security Hub for compliance monitoring

**📝 Audit Ready**

- CloudTrail logging to encrypted S3
- VPC Flow Logs for network monitoring
- RDS audit logging enabled
- All logs retained for 7 years (HIPAA minimum: 6)

**💾 Data Protection**

- KMS encryption for all data stores
- Automated daily backups with cross-region replication
- S3 versioning and MFA delete protection
- RDS automated snapshots with 35-day retention

**🌐 Network Architecture**

- Multi-AZ deployment for high availability
- Private subnets for databases and internal services
- NAT Gateways for secure outbound access
- VPC endpoints for AWS services (no internet exposure)

## Usage

```hcl
module "hipaa_infrastructure" {
  source  = "ummahrican/hipaa/aws"
  version = "2.1.0"

  environment     = "production"
  project_name    = "my-health-app"
  aws_region      = "us-east-1"

  # VPC Configuration
  vpc_cidr           = "10.0.0.0/16"
  availability_zones = ["us-east-1a", "us-east-1b", "us-east-1c"]

  # Database
  db_instance_class = "db.r6g.large"
  db_name           = "healthapp"

  # Compliance
  enable_guardduty     = true
  enable_security_hub  = true
  log_retention_days   = 2557  # 7 years

  tags = {
    Compliance = "HIPAA"
    DataClass  = "PHI"
  }
}
```

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                         AWS Cloud                                │
│  ┌───────────────────────────────────────────────────────────┐  │
│  │                          VPC                               │  │
│  │  ┌─────────────────┐       ┌─────────────────┐           │  │
│  │  │ Public Subnet   │       │ Public Subnet   │           │  │
│  │  │   (AZ-1)        │       │   (AZ-2)        │           │  │
│  │  │  ┌───────────┐  │       │  ┌───────────┐  │           │  │
│  │  │  │    ALB    │  │       │  │    NAT    │  │           │  │
│  │  │  └───────────┘  │       │  └───────────┘  │           │  │
│  │  └─────────────────┘       └─────────────────┘           │  │
│  │  ┌─────────────────┐       ┌─────────────────┐           │  │
│  │  │ Private Subnet  │       │ Private Subnet  │           │  │
│  │  │   (AZ-1)        │       │   (AZ-2)        │           │  │
│  │  │  ┌───────────┐  │       │  ┌───────────┐  │           │  │
│  │  │  │    ECS    │◄─┼───────┼─►│    ECS    │  │           │  │
│  │  │  └───────────┘  │       │  └───────────┘  │           │  │
│  │  └─────────────────┘       └─────────────────┘           │  │
│  │  ┌─────────────────┐       ┌─────────────────┐           │  │
│  │  │   DB Subnet     │       │   DB Subnet     │           │  │
│  │  │   (AZ-1)        │       │   (AZ-2)        │           │  │
│  │  │  ┌───────────┐  │       │  ┌───────────┐  │           │  │
│  │  │  │  RDS Pri  │◄─┼───────┼─►│  RDS Sec  │  │           │  │
│  │  │  └───────────┘  │       │  └───────────┘  │           │  │
│  │  └─────────────────┘       └─────────────────┘           │  │
│  └───────────────────────────────────────────────────────────┘  │
│                                                                  │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  CloudTrail  │  │  GuardDuty   │  │ Security Hub │          │
│  │   (Audit)    │  │  (Threats)   │  │ (Compliance) │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
└─────────────────────────────────────────────────────────────────┘
```

## Compliance Mappings

The module addresses these HIPAA technical safeguards:

| HIPAA Requirement                   | Implementation                       |
| ----------------------------------- | ------------------------------------ |
| Access Control (§164.312(a))        | IAM roles, Security Groups, NACLs    |
| Audit Controls (§164.312(b))        | CloudTrail, VPC Flow Logs, RDS Audit |
| Integrity Controls (§164.312(c))    | S3 versioning, RDS snapshots         |
| Transmission Security (§164.312(e)) | TLS 1.2+, ACM certificates           |
| Encryption (§164.312(a)(2)(iv))     | KMS encryption everywhere            |

## Community Impact

Since release, the module has been:

- ⭐ **850+ GitHub stars**
- 📦 **15,000+ downloads** from Terraform Registry
- 🏥 **50+ healthcare organizations** using in production
- 🔒 **0 security vulnerabilities** reported

## Contributing

The project welcomes contributions. Areas where help is needed:

1. Azure and GCP equivalents
2. Additional compliance frameworks (SOC 2, HITRUST)
3. Cost optimization configurations
4. Documentation translations

## License
