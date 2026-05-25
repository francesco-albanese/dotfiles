# Operations Reference

## Makefile Commands

```bash
# Initialize terraform with state.conf
make environmental-init ACCOUNT=sandbox AWS_PROFILE=sandbox-admin

# Plan changes
make environmental-plan ACCOUNT=staging AWS_PROFILE=staging-admin

# Apply changes
make environmental-apply ACCOUNT=production AWS_PROFILE=production-admin

# Format code
make fmt

# Clean .terraform/
make environmental-clean

# CI/CD (OIDC — empty AWS_PROFILE skips profile prefix)
make environmental-plan ACCOUNT=sandbox AWS_PROFILE=
```

## Customization Points

**state.conf**:
- `bucket`: S3 bucket name for state
- `role_arn`: IAM role for cross-account access
- `region`: AWS region
- `key`: Not in state.conf — passed per-stack via Makefile (see terraform.mk)

**providers.tf**:
- Default tags (change `franco:` prefix)
- Terraform role name (currently `terraform`)

**env/*.tfvars**:
- `account_id`: AWS account ID
- `account_name`: Environment name
- `region`: AWS region

**GitHub Actions**:
- Workflow triggers (push to main, PR, manual)
- Environment approval rules
- AWS credentials configuration

**Cross-Account Trust (GitHub OIDC)**:
- Shared-services terraform role must trust target account terraform roles
- Target account roles need OIDC trust + ability to assume shared-services role
- See [architecture.md](architecture.md#github-oidc--cross-account-state-access) for setup

## GitHub Actions Integration

Generated workflow:
- Defaults to sandbox environment
- Requires manual approval for staging/uat/production
- Uses OIDC or AWS credentials from secrets
- Runs terraform init/plan/apply with appropriate flags
- Supports multiple environments in single workflow

Configure AWS credentials in GitHub:
- OIDC (recommended): Configure trust relationship
- Secrets: `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`

## Security Patterns

- **Assume role**: Cross-account access via terraform role
- **State encryption**: SSE-S3 (free) not SSE-KMS
- **Default tags**: Track resources by stack/environment/managed_by
- **External ID**: Cross-account security (if needed)
- **Public access blocked**: S3 bucket hardened
- **GitIgnore**: state.conf, *.tfvars, .terraform/

## Common Operations

**Add new environment**:
1. Create `env/<new-env>.tfvars`
2. Add Make variables in `makefiles/terraform.mk`
3. Update GitHub Actions matrix

**Change state backend**:
1. Update `state.conf`
2. Run `make environmental-init ACCOUNT=<env>`
3. Migrate state if needed

**Switch AWS profile**:
```bash
make environmental-plan ACCOUNT=sandbox AWS_PROFILE=my-profile
```
