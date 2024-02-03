import re
import os
import logging
import random
from slack_bolt import App

logging.basicConfig(level=logging.DEBUG)

# Slack App Config
app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET"),
    process_before_response=True,
)

@app.message(re.compile("([a-zA-Z0-9-]+)\+\+"))
def handle_message(message, say, context):
    for matched_text in context['matches']:
        patterns = (f"{matched_text}がプラプラされたよ. ", f"{matched_text} いいね!", f"{matched_text} ナイス!")
        counter = random.randint(0, 100)
        reply = random.choice(patterns) + f" (++された回数: {counter})"
        say(reply)

# @app.message("hello")
# def message_hello(message, say):
#     say(f"Hey there <@{message['user']}>!")

if __name__ == "__main__":
    from slack_bolt.adapter.socket_mode import SocketModeHandler
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()

from slack_bolt.adapter.aws_lambda import SlackRequestHandler

# Logging for AWS Lambda
SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

# AWS Lambda support
def lambda_handler(event, context):
    slack_handler = SlackRequestHandler(app)
    return slack_handler.handle(event, context)
