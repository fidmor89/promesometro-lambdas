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

if [ "$1" != "" ]; then
  cd services/$1
  if [ "$2" != "" ]; then
    FUNCTION=$1'-'$2
    FILE=$2'.py'
    PACKAGE=$FILE'.zip'

    echo $FUNCTION
    echo $FILE
    echo $PACKAGE

    # Install dependencies
    pip install pymysql -t $PWD

    # Create deployment package
    zip -r $PACKAGE $FILE PyMySQL-0.9.3.dist-info pymysql

    # TODO: Set enviroment variables.

    # Deploy
    aws lambda update-function-code --function-name $FUNCTION --zip-file fileb://$PACKAGE

    # Clean-up
    rm -rf PyMySQL-0.9.3.dist-info
    rm -rf pymysql
    rm -rf $PACKAGE

  else
    echo "Need the function name"
    ls -l
    exit 1
  fi
else
  echo "Need directory for function"
  exit 1
fi
