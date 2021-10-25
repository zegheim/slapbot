# slapbot
Slap your friends in Telegram.


## Development

### Telegram webhook input

When Telegram hits our endpoint, our lambda function will receive the following payload under `event`:

```
{
    'version': '2.0', 
    'routeKey': 'POST /slap/{token}', 
    'rawPath': '/slap/123:xxx', 
    'rawQueryString': '', 
    'headers': {
        'accept-encoding': 'gzip, deflate', 
        'content-length': '123', 
        'content-type': 'application/json', 
        'host': 'xxx.execute-api.xxx.amazonaws.com', 
        'x-amzn-trace-id': 'xxx', 
        'x-forwarded-for': 'xxx', 
        'x-forwarded-port': '443', 
        'x-forwarded-proto': 'https'
    }, 
    'requestContext': {
        'accountId': '123', 
        'apiId': 'xxx', 
        'authorizer': {
            'lambda': None
        }, 
        'domainName': 'xxx.execute-api.xxx.amazonaws.com', 
        'domainPrefix': 'xxx', 
        'http': {
            'method': 'POST', 
            'path': '/slap/123:xxx', 
            'protocol': 'HTTP/1.1', 
            'sourceIp': 'xxx', 'userAgent': ''}, 
            'requestId': 'xxx', 
            'routeKey': 'POST /slap/{token}', 
            'stage': '$default', 
            'time': '01/Jan/1970:00:00:00 +0000', 
            'timeEpoch': 0
    }, 
    'pathParameters': {
        'token': '123:xxx'
    }, 
    'body': '{"update_id":123,\n"message":{"message_id":1,"from":{"id":123,"is_bot":false,"first_name":"John","last_name":"Doe","username":"johndoe"},"chat":{"id":-123,"title":"Test","type":"group","all_members_are_administrators":true},"date":0,"text":"/slap @johndoe","entities":[{"offset":0,"length":5,"type":"bot_command"},{"offset":6,"length":8,"type":"mention"}]}}', 
    'isBase64Encoded': False
}
```

