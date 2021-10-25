# slapbot
Slap your friends in Telegram.

## Setup

### Pre-requisites

You would need to install the following in your account:

- [Python 3.9](https://www.python.org/downloads/release/python-390/)
- [Poetry](https://python-poetry.org/)
- [serverless CLI](https://www.serverless.com/)
- [curl](https://curl.se/)

You would also need to have an [AWS](https://aws.amazon.com/) account and connect it to serverless from the CLI.

### Steps

1. Create a bot by talking to BotFather following the steps listed [here](https://core.telegram.org/bots#3-how-do-i-create-a-bot), and make a note of your bot token.
2. Still in the BotFather chat, use the `/setcommands` command and register the `slap` command.
3. Copy `.env.example` to `.env`, and fill in the blanks with your bot token and bot username (don't include the `@` symbol). You may also wish to set `AWS_REGION` to a different region.
4. Copy `config/tools.py.example` to `config/tools.py`. Feel free to replace the contents of `SLAP_TOOL` with your own content.
5. Run `serverless deploy --verbose`. Assuming you've linked your AWS account to the serverless CLI, this should automatically provision all necessary resources to get your bot up and running. The CLI will output your bot endpoint (under endpoints -> POST) - make a note of this.
6. Run the following command (make sure to replace `<TOKEN>` with your actual bot token and `url` with your actual endpoint):

    ```
    curl --request POST --url https://api.telegram.org/bot<TOKEN>/setWebhook --header 'content-type: application/json' --data '{"url": "https://abcdefg.execute-api.us-east-1.amazonaws.com/slap/<TOKEN>"}'
    ```
    
    This registers a webhook which the Bot API automatically calls whenever it receives a message.

## Commands

Currently this bot only supports one command.
### `/slap <user1> <user2>`
The `/slap` command slaps the tagged user using a random tool defined in `config/tools.py`. 

If no argument is passed, this command slaps the sender instead.

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

