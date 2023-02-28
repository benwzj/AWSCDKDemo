# CDK Python Demo Project!

```
cdk deploy
```

This Demo create two REST APIs:

- One for Url Shortener,
- Another one is Widgets.

## Url Shortener

Using a short string to route to the RUL which you store in the dymamoDB table.

```
https://GUID.execute-api.REGION.amazonaws.com/prod/

usage: ?targetUrl=URL
```

## Widgets

you can store object in S3 by using POST, like:

```
curl -X GET 'https://GUID.execute-api.REGION.amazonaws.com/prod'
curl -X POST 'https://GUID.execute-api.REGION.amazonaws.com/prod/example'
curl -X GET 'https://GUID.execute-api.REGION.amazonaws.com/prod'
curl -X GET 'https://GUID.execute-api.REGION.amazonaws.com/prod/example'
curl -X DELETE 'https://GUID.execute-api.REGION.amazonaws.com/prod/example'
curl -X GET 'https://GUID.execute-api.REGION.amazonaws.com/prod'
```
