#!/bin/bash
set -euo pipefail
. /usr/share/install-libraries/il-lib.sh

emit_step "Remove old msa_sdk folders."
color mkdir -p /opt/fmc_repository/Process/PythonReference
color rm -Rf /opt/fmc_repository/Process/PythonReference/msa_sdk*
color ln -sf /opt/fmc_repository/python-sdk/msa_sdk /opt/fmc_repository/Process/PythonReference/msa_sdk
emit_step "Create custom folder."
color mkdir -p /opt/fmc_repository/Process/PythonReference/custom
touch /opt/fmc_repository/Process/PythonReference/custom/__init__.py
