#!/bin/sh

#  Deploy.sh
#
#  Created by Fidel Esteban Morales Cifuentes on 7/5/19.
#

# A script to build and deploy a lambda funtion

# To set executeable permissions the first time:
# Open terminal and run:
# chmod +x deploy.sh

# Cancel on error.
set -o errexit

publish()
{
    FUNCTION=$1'-'$2
    FILE=$2'.py'
    PACKAGE=$FILE'.zip'

    echo $FUNCTION
    echo $FILE
    echo $PACKAGE

    # Create deployment package
    zip -r $PACKAGE $FILE PyMySQL-0.9.3.dist-info pymysql

    # TODO: Set enviroment variables.

    # Deploy
    aws lambda update-function-code --function-name $FUNCTION --zip-file fileb://$PACKAGE

    # Clean up package
    rm -rf $PACKAGE
}

dependencies() {
    # Install dependencies
    pip install pymysql -t $PWD
}

cleanup() {
    # Clean-up
    rm -rf PyMySQL-0.9.3.dist-info
    rm -rf pymysql
}

if [ "$1" != "" ]; then
  cd services/$1
  if [ "$2" != "" ]; then
    dependencies
    publish $1 $2
    cleanup
    exit 0
  else
    echo "Deploying all services"

    dependencies
    publish $1 "delete"
    publish $1 "get"
    publish $1 "post"
    publish $1 "put"
    cleanup

    exit 0
  fi
else
  echo "Need directory for function"
  exit 1
fi
