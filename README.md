# promesometro-lambdas

Python lambdas for promesometro project

## Python lambdas ##

### To get dependencies ###

```
pip install pymysql --target
```

### To deploy a single function ###

```
./deploy.sh party get
```

### To deploy all functions for a service ###

```
./deploy.sh party
```


## API-Gateway ##

### Get configuration ###

```
aws configure

aws apigateway get-export --parameters extensions='apigateway' --rest-api-id uhwvsjvsme --stage-name dev --export-type swagger promesometro.json
```
