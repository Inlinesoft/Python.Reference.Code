Based on https://gist.github.com/ca0abinary/e4825841d47d987ffc78ed62e5619055

Lambda layer is generated from source (while local dev and pipeline uses prebuilt packages)


Generate layer files:

```
docker build -t pyodbc .
docker run -d --name pyodbc pyodbc true
docker cp pyodbc:/python-odbc.zip .
docker rm -f pyodbc &> /dev/null

unzip python-odbc.zip -d python-odbc
```


Run serverless to upload layer:
```
serverless deploy --stage dev
```