# Slack Bot

## Development

### Set up development env

1. Create venv with Python

```
python -m venv env
source env/bin/activate
```

2. Install packages

```
pip install -r requirements.txt
```

3. Start app

```
python main.py
```

4. Start tunneling

```
make tunnel
```

5. Change "Request URL" for Event Subscriptions on Slack API console

```
Event Subscriptions -> Enable Events ->  Request URL
```

![Setting Page](image.png)

## Slack App Manifest

```
display_information:
  name: tmykbot
features:
  bot_user:
    display_name: tmykbot
    always_online: false
oauth_config:
  redirect_urls:
    - https://forty-pears-fly.loca.lt/slack/events
  scopes:
    bot:
      - app_mentions:read
      - chat:write
      - chat:write.public
      - channels:history
      - groups:history
settings:
  event_subscriptions:
    request_url: https://forty-pears-fly.loca.lt/slack/events
    bot_events:
      - message.channels
      - message.groups
  org_deploy_enabled: false
  socket_mode_enabled: false
  token_rotation_enabled: false
```

### Deploy a bot to Lambda

Install serverless framework

```
npm install -g serverless
```

Install plugins for serverless framework

```
serverless plugin install -n serverless-python-requirements
```