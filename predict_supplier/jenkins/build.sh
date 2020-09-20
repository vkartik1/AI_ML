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
PYTHON_PIP_PYTEST_PATH=/Users/vkartik/anaconda/anaconda3/bin
PATH=$PYTHON_PIP_PYTEST_PATH:$PATH

pip install -r ${PROJECT_ROOT_DIR}/src/requirements.txt
python src/model_supplier.py 
