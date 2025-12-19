#!/usr/bin/env bash
# vim: set filetype=sh tabstop=4 shiftwidth=4 expandtab cursorline ruler |
#
# A simple script to be run after a release is created.
# You can update the version in the main branch to the next development version.
# This script assumes that the release version and next version are passed as environment variables.
#
# Credentials to push to the repository should be set up in the GitHub Actions environment.
#
# Usage:
#   RELEASE_VERSION=1.2.3 RELEASE_NEXT_VERSION=1.2.4 bash .github/after-release.sh
#
# NOTE: Git setup (user.name, user.email) is configured in the GitHub Actions workflow.
#       To run this script locally, ensure your git user is configured.
#

BOLD="\033[1m"
RED="\033[31m"
GREEN="\033[32m"
YELLOW="\033[33m"
BLUE="\033[34m"
MAGENTA="\033[35m"
RESET="\033[0m"

set -e

echo -e "${BOLD}${BLUE}🚀 Starting post-release version update...${RESET}"

# Get the release version and next version from environment variables
release_version="${RELEASE_VERSION}"
next_version="${RELEASE_NEXT_VERSION}"

if [[ -z "$release_version" || -z "$next_version" ]]; then
    echo -e "${BOLD}${RED}❌ ERROR: RELEASE_VERSION and RELEASE_NEXT_VERSION environment variables must be set.${RESET}"
    exit 1
fi

echo -e "${BOLD}${YELLOW}🔖 Updating main branch to next development version: ${next_version}${RESET}"
#
# Current branch is assumed to be release/*
#

#git push
#
# Checkout master branch
#
git checkout master

pushd ..
python -m pip install --upgrade pip
python -m pip install bump2version
popd
bump2version --new-version "${next_version}" msa_sdk/__init__.py
git add msa_sdk/__init__.py .bumpversion.cfg
git commit -m "🎉 Bump version to ${next_version}"

echo -e "${BOLD}${GREEN}✅ Version updated to ${next_version} and committed to master branch.${RESET}"
# Push the changes to the remote repository
git push origin master
echo -e "${GREEN}🚀 Changes pushed to remote repository successfully!${RESET}"
