---
name: terraform-bootstrap
description: Bootstrap Terraform projects with multi-account AWS patterns, centralized state management, and CI/CD. Use when bootstrapping, initializing, or scaffolding a new Terraform project, setting up AWS infrastructure folder structure, or starting a new terraform configuration.
argument-hint: "[project-name]"
allowed-tools: Bash, Write, Read, AskUserQuestion
---

# Terraform Bootstrap

Bootstrap Terraform projects with multi-account AWS architecture patterns, centralized state management, and CI/CD integration.

## Quick Start

When user requests terraform project initialization:

1. **Run bootstrap script**:
   ```bash
   python ~/.claude/skills/terraform-bootstrap/scripts/bootstrap_project.py --project-name <name> [--output-dir <path>]
   ```

2. **Customize generated files**:
   - Update `state.conf` with actual S3 bucket name and shared-services account ID (key is passed per-stack via Makefile)
   - Adjust account IDs in `env/*.tfvars`
   - Modify default tags in `providers.tf`

3. **Initialize terraform**:
   ```bash
   make environmental-init ACCOUNT=sandbox AWS_PROFILE=sandbox-admin
   ```

4. **CI/CD**: Pass `AWS_PROFILE=` (empty) to skip profile prefix when using OIDC env vars:
   ```bash
   make environmental-plan ACCOUNT=sandbox AWS_PROFILE=
   ```

## Architecture Pattern

Multi-account AWS setup:
- **Environments**: sandbox, staging, uat, production
- **State**: Centralized S3 + DynamoDB in shared-services account
- **Access**: Terraform role with admin privileges via assume_role
- **CI/CD**: GitHub Actions defaulting to sandbox, manual promotion

For detailed architecture, see [architecture.md](references/architecture.md).

## Project Structure

Bootstrap creates:
```
<project-name>/
├── state.conf                          # S3 backend config (gitignored)
├── Makefile                            # Root makefile
├── makefiles/
│   └── terraform.mk                    # Terraform automation
├── terraform/
│   └── environmental/
│       ├── main.tf                     # Resources (initially empty)
│       ├── providers.tf                # AWS provider + assume_role + default_tags
│       ├── terraform.tf                # Backend S3 config + versions
│       ├── variables.tf                # Input variables
│       ├── outputs.tf                  # Outputs
│       └── env/
│           ├── sandbox.tfvars          # Sandbox config
│           ├── staging.tfvars          # Staging config
│           ├── uat.tfvars              # UAT config
│           └── production.tfvars       # Production config
└── .github/
    └── workflows/
        └── terraform-deploy.yml        # CI/CD workflow
```

## Workflow

1. **Bootstrap**: Run script, creates structure
2. **Configure**: Update state.conf, account IDs, tags
3. **Init**: `make environmental-init ACCOUNT=sandbox`
4. **Develop**: Add resources to main.tf
5. **Deploy**: Push to GitHub → Actions runs → Deploys to sandbox
6. **Promote**: Manual workflow dispatch for staging/uat/production

## Additional Resources

- [Architecture details](references/architecture.md)
- [Commands, customization, operations](references/operations.md)
