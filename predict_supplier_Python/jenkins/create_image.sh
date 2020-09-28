#!/bin/bash
#
# This is called from the jenkins "Execute shell", to create the docker image
#   $1 being the project root directory define in the Jenkins as "String Parameter"
#   $2 being the standard jenkins env variable WORKSPACE
#

PROJECT_ROOT_DIR=$1
JENKINS_WORKSPACE_DIR=$2
echo "create image Path: "$PATH

cd ${PROJECT_ROOT_DIR}
docker-compose build

