#!/bin/bash
#
# This is called from the jenkins "Execute shell", as part of the ** Build ** stage, with,
#   $1 being the project root directory define in the Jenkins as "String Parameter"
#   $2 being the standard jenkins env variable WORKSPACE
#

#####
# Relace the the PYTHON_PIP_PYTEST_PATH value with the right loction of the pytest, pip, and python
####
PROJECT_ROOT_DIR=$1
JENKINS_WORKSPACE_DIR=$2
cd ${PROJECT_ROOT_DIR}

# Its ok if uninstall errors out when chart doesnt exist
helm uninstall predict-suppplier-chart >& /dev/null
echo "About to install chart"
helm install predict-suppplier-chart supplier-chart/ --values $PROJECT_ROOT_DIR/supplier-chart/values.yaml
