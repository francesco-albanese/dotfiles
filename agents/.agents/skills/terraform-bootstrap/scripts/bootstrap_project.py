#!/usr/bin/env python3
"""
Bootstrap a new Terraform project with multi-account AWS patterns.
"""

import argparse
import os
import shutil
from pathlib import Path


def create_directory_structure(output_dir: Path) -> dict:
    """Create the project directory structure."""
    dirs = {
        'root': output_dir,
        'makefiles': output_dir / 'makefiles',
        'terraform': output_dir / 'terraform',
        'environmental': output_dir / 'terraform' / 'environmental',
        'env': output_dir / 'terraform' / 'environmental' / 'env',
        'github': output_dir / '.github' / 'workflows',
    }

    for dir_path in dirs.values():
        dir_path.mkdir(parents=True, exist_ok=True)

    return dirs


def copy_templates(asset_dir: Path, dirs: dict, project_name: str):
    """Copy template files to project directory."""

    # Copy terraform files
    tf_templates = asset_dir / 'terraform' / 'environmental'
    for tf_file in ['main.tf', 'providers.tf', 'terraform.tf', 'variables.tf', 'outputs.tf']:
        src = tf_templates / tf_file
        dst = dirs['environmental'] / tf_file
        if src.exists():
            shutil.copy2(src, dst)
            # Substitute project name in providers.tf
            if tf_file == 'providers.tf':
                content = dst.read_text()
                content = content.replace('aws-multi-account-sso', project_name)
                dst.write_text(content)

    # Copy env tfvars templates
    env_templates = tf_templates / 'env'
    for env in ['sandbox', 'staging', 'uat', 'production']:
        src = env_templates / f'{env}.tfvars.template'
        dst = dirs['env'] / f'{env}.tfvars'
        if src.exists():
            shutil.copy2(src, dst)

    # Copy Makefile
    makefile_src = asset_dir / 'Makefile'
    makefile_dst = dirs['root'] / 'Makefile'
    if makefile_src.exists():
        content = makefile_src.read_text()
        content = content.replace('aws-multi-account', project_name)
        makefile_dst.write_text(content)

    # Copy makefiles/terraform.mk
    terraform_mk_src = asset_dir / 'makefiles' / 'terraform.mk'
    terraform_mk_dst = dirs['makefiles'] / 'terraform.mk'
    if terraform_mk_src.exists():
        shutil.copy2(terraform_mk_src, terraform_mk_dst)

    # Copy state.conf template
    state_conf_src = asset_dir / 'state.conf.template'
    state_conf_dst = dirs['root'] / 'state.conf'
    if state_conf_src.exists():
        shutil.copy2(state_conf_src, state_conf_dst)

    # Copy GitHub Actions workflow
    workflow_src = asset_dir / '.github' / 'workflows' / 'terraform-deploy.yml'
    workflow_dst = dirs['github'] / 'terraform-deploy.yml'
    if workflow_src.exists():
        shutil.copy2(workflow_src, workflow_dst)


def create_gitignore(output_dir: Path):
    """Create .gitignore file."""
    gitignore_content = """# Local .terraform directories
**/.terraform/*

# .tfstate files
*.tfstate
*.tfstate.*

# Crash log files
crash.log
crash.*.log

# Exclude all .tfvars files (may contain sensitive data)
*.tfvars
*.tfvars.json

# Override files
override.tf
override.tf.json
*_override.tf
*_override.tf.json

# CLI configuration files
.terraformrc
terraform.rc

# State configuration (contains sensitive info)
state.conf

# Lock files (optional - some teams commit this)
.terraform.lock.hcl
"""
    gitignore_path = output_dir / '.gitignore'
    gitignore_path.write_text(gitignore_content)


def main():
    parser = argparse.ArgumentParser(
        description='Bootstrap a Terraform project with multi-account AWS patterns'
    )
    parser.add_argument(
        '--project-name',
        required=True,
        help='Name of the project (e.g., my-aws-project)'
    )
    parser.add_argument(
        '--output-dir',
        default='.',
        help='Output directory (default: current directory)'
    )

    args = parser.parse_args()

    # Setup paths
    output_dir = Path(args.output_dir).resolve() / args.project_name
    script_dir = Path(__file__).parent
    skill_dir = script_dir.parent
    asset_dir = skill_dir / 'assets'

    print(f"🚀 Bootstrapping Terraform project: {args.project_name}")
    print(f"   Output directory: {output_dir}")

    # Create structure
    print("\n📁 Creating directory structure...")
    dirs = create_directory_structure(output_dir)

    # Copy templates
    print("📄 Copying template files...")
    copy_templates(asset_dir, dirs, args.project_name)

    # Create .gitignore
    print("🔒 Creating .gitignore...")
    create_gitignore(output_dir)

    print(f"\n✅ Project bootstrapped successfully!")
    print(f"\nNext steps:")
    print(f"1. cd {output_dir}")
    print(f"2. Update state.conf with your S3 bucket and IAM role")
    print(f"3. Update env/*.tfvars with your AWS account IDs")
    print(f"4. Update default_tags in terraform/environmental/providers.tf")
    print(f"5. Run: make environmental-init ACCOUNT=sandbox")


if __name__ == '__main__':
    main()
