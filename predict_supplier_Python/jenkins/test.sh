#!/bin/bash

#
# This is called from the jenkins "Execute shell", as part of the ** Test ** stage, with,
#   $1 being the project root directory define in the Jenkins as "String Parameter"
#   $2 being the standard jenkins env variable WORKSPACE
#
# The "Post-build Actions" stage of Jenkins has a field "Test report XMLs" which takes the Junit style results file from the pytest output. It expects
# the results to be under a diretcory whose root directory is jenkins WORKSPACE dirc
#
PROJECT_ROOT_DIR=$1
JENKINS_WORKSPACE_DIR=$2

cd ${PROJECT_ROOT_DIR}
pytest --junit-xml=$JENKINS_WORKSPACE_DIR/predict_supplier_results.xml
