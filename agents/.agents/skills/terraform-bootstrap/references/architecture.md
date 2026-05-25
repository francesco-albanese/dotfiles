# Multi-Account AWS Architecture Patterns

## Overview

Production-grade AWS multi-account architecture with centralized state management, environment separation, and GitOps workflows.

## Architecture Components

### Account Structure

```
Management Account (Root)
  ├── AWS Organizations
  ├── IAM Identity Center (SSO)
  └── Terraform execution context

Shared-Services Account
  ├── S3 bucket (terraform state) - SSE-S3 encryption
  ├── DynamoDB table (state locking)
  └── IAM role: terraform (cross-account access)

Environmental Accounts (4)
  ├── sandbox     - Development and testing
  ├── staging     - Pre-production validation
  ├── uat         - User acceptance testing
  └── production  - Live workloads
```

### Cross-Account Access Pattern

Terraform authenticates to management account, then assumes role into target account:

1. Authenticate to management account (via AWS profile)
2. Terraform calls AWS STS AssumeRole API
3. AWS validates management account in terraform role's trust policy
4. AWS returns temporary credentials (valid 1 hour)
5. Terraform uses temp credentials for API calls

**Trust Policy** (in target account's terraform role):
```json
{
  "Principal": {
    "AWS": "arn:aws:iam::<management-account-id>:root"
  }
}
```

## State Management

### Centralized State Backend

All terraform state stored in shared-services account:

- **S3 bucket**: Versioned, encrypted (SSE-S3), public access blocked
- **DynamoDB table**: State locking, PAY_PER_REQUEST billing
- **Access pattern**: Assume terraform role in shared-services
- **State keys**: `<stack>/<env>/terraform.tfstate`

### state.conf Pattern

Backend configuration externalized to `state.conf` file (gitignored):

```hcl
bucket       = "<bucket-name>"
# key passed per-stack via Makefile (see terraform.mk)
region       = "eu-west-2"
use_lockfile = true
encrypt      = true
assume_role = {
  role_arn = "arn:aws:iam::<account-id>:role/terraform"
}
```

Initialize with: `make environmental-init ACCOUNT=sandbox`

## Separation of Concerns

### Directory Structure

```
terraform/
└── environmental/              # Environment-specific resources
    ├── main.tf                # Resource definitions
    ├── providers.tf           # AWS provider + assume_role
    ├── terraform.tf           # Backend config + versions
    ├── variables.tf           # Input variables
    ├── outputs.tf             # Outputs
    └── env/
        ├── sandbox.tfvars     # Sandbox config
        ├── staging.tfvars     # Staging config
        ├── uat.tfvars         # UAT config
        └── production.tfvars  # Production config
```

### Stack Pattern

Each stack (environmental, shared-services, etc.) is self-contained:

- Own `main.tf`, `providers.tf`, `terraform.tf`
- Environment-specific tfvars in `env/` subdirectory
- Backend configured via `state.conf`
- Independent lifecycle (init, plan, apply)

## Default Tags

All resources tagged automatically via `default_tags` in provider:

```hcl
provider "aws" {
  default_tags {
    tags = {
      "<org>:terraform_stack" = "<project-name>"
      "<org>:managed_by"      = "terraform"
      "<org>:environment"     = var.account_name
    }
  }
}
```

Replace `<org>` prefix with your organization identifier.

## Terraform Role

IAM role in each account with:

- **Name**: `terraform`
- **Trust policy**: Trusts management account
- **Permissions**: AdministratorAccess (or scoped permissions)
- **Used by**: Local CLI and GitHub Actions

## GitHub Actions CI/CD

### Workflow Pattern

```yaml
on:
  push:
    branches: [main]
  pull_request:
  workflow_dispatch:
    inputs:
      environment:
        type: choice
        options: [sandbox, staging, uat, production]
```

### Environment Strategy

- **Default**: Deploy to sandbox on push to main
- **Manual**: workflow_dispatch for staging/uat/production
- **Protection**: Environment rules for production approval

### Authentication

**Option 1: OIDC (Recommended)**
- Configure AWS OIDC provider
- Trust relationship on terraform role
- No long-lived credentials

**Option 2: Secrets**
- Store `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`
- Use service account with AssumeRole permissions

### Workflow Steps

1. Checkout code
2. Configure AWS credentials
3. Setup Terraform
4. `terraform init -backend-config=state.conf`
5. `terraform plan -var-file=env/${{ env }}.tfvars`
6. `terraform apply -auto-approve` (main branch only)

## GitHub OIDC + Cross-Account State Access

When using GitHub Actions with OIDC and centralized state in shared-services, a **role chaining** pattern is required.

### Why Role Chaining

- GitHub OIDC authenticates to **target account** terraform role (sandbox, staging, etc.)
- Terraform state lives in **shared-services account**
- Target account role must be able to assume shared-services role for state access

This pattern follows [AWS Control Tower AFT](https://docs.aws.amazon.com/controltower/latest/userguide/aft-overview.html) and [HashiCorp best practices](https://developer.hashicorp.com/terraform/tutorials/aws/aws-assumerole).

### Authentication Flow

```
GitHub Actions
    ↓
OIDC Token (id-token: write permission)
    ↓
AWS STS AssumeRoleWithWebIdentity
    ↓
Target Account Terraform Role (e.g., sandbox)
    ↓
Terraform Init
    ├── Backend: AssumeRole → Shared-Services Role → S3 State
    └── Provider: Uses Target Account Role → Create Resources
```

### Required Trust Configuration

**Shared-services terraform role** must trust all target account terraform roles:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "AWS": [
          "arn:aws:iam::<management-account-id>:root",
          "arn:aws:iam::<sandbox-account-id>:role/terraform",
          "arn:aws:iam::<staging-account-id>:role/terraform",
          "arn:aws:iam::<uat-account-id>:role/terraform",
          "arn:aws:iam::<production-account-id>:role/terraform"
        ]
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
```

**Target account terraform roles** need:
1. GitHub OIDC trust (for initial auth)
2. `sts:AssumeRole` permission for shared-services role (usually via AdministratorAccess)

### GitHub OIDC Trust Policy (Target Accounts)

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Federated": "arn:aws:iam::<account-id>:oidc-provider/token.actions.githubusercontent.com"
      },
      "Action": "sts:AssumeRoleWithWebIdentity",
      "Condition": {
        "StringEquals": {
          "token.actions.githubusercontent.com:aud": "sts.amazonaws.com"
        },
        "StringLike": {
          "token.actions.githubusercontent.com:sub": "repo:<org>/<repo>:*"
        }
      }
    }
  ]
}
```

### Why This Pattern is Best Practice

| Benefit | Description |
|---------|-------------|
| **Security** | Temporary credentials via AssumeRole, not long-lived keys |
| **Audit** | CloudTrail logs all role assumptions for compliance |
| **Centralized** | Single state location, consistent governance |
| **Scalable** | AWS Control Tower AFT pattern, used by enterprises |

### Setup Checklist

- [ ] Create OIDC provider in each target account
- [ ] Add OIDC trust to target account terraform roles
- [ ] Add target account roles to shared-services trust policy
- [ ] Configure per-environment role ARNs in GitHub secrets
- [ ] Verify with `gh workflow run terraform-deploy.yml -f environment=sandbox`

## Security Features

### Encryption
- S3 state: SSE-S3 (AES-256) - FREE
- DynamoDB: Encrypted at rest (default)
- Transit: TLS 1.2+

### Access Control
- Assume role cross-account access
- External ID (optional for third-party access)
- Least privilege via permission sets

### GitOps Security
- state.conf gitignored (contains sensitive ARNs)
- *.tfvars gitignored (may contain account IDs)
- .terraform/ gitignored
- S3 bucket versioning for state recovery

## Cost Optimization

Zero-cost architecture leveraging free tiers:

- ✅ SSE-S3 (not SSE-KMS): FREE
- ✅ S3 free tier: 50GB (state files ~KB)
- ✅ DynamoDB free tier: 25GB, 25 RCU/WCU
- ✅ IAM Identity Center: $0 for AWS assignments

Expected cost: $0-1/month

## Common Patterns

### Adding New Environment

1. Create `env/<new-env>.tfvars`
2. Add Make variables in `makefiles/terraform.mk`:
   ```make
   <new-env>_KEY := $(PROJECT_NAME)
   <new-env>_ACCOUNT := <new-env>
   <new-env>_FLAGS := -var-file=env/<new-env>.tfvars
   ```
3. Update GitHub Actions matrix

### Multi-Region Deployment

Use provider aliases:

```hcl
provider "aws" {
  alias  = "us-east-1"
  region = "us-east-1"
  assume_role {
    role_arn = "arn:aws:iam::${var.account_id}:role/terraform"
  }
}
```

### Shared Resources

Create separate stack for shared resources:

```
terraform/
├── environmental/    # Per-environment resources
└── shared-services/  # Cross-account shared resources
```

## Troubleshooting

**State access denied**
- Verify terraform role exists in target account
- Check trust policy includes management account
- Confirm role ARN in state.conf is correct

**Account creation slow**
- AWS takes 5-10 min per account
- Use `terraform apply -target` for incremental creation

**Init fails on backend**
- Ensure state.conf exists and has correct values
- Verify S3 bucket and DynamoDB table exist
- Check AWS credentials have AssumeRole permissions

**GitHub Actions fails**
- Verify AWS credentials/OIDC configured
- Check terraform role trust relationship
- Ensure state.conf values are in GitHub secrets
