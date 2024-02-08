try:
    import unzip_requirements
except ImportError:
    pass

import logging
import os
import random
import re

import boto3
from slack_bolt import App

logging.basicConfig(level=logging.DEBUG)

# Slack App Config
app = App(
    signing_secret=os.getenv("SLACK_SIGNING_SECRET"),  # Required for Event Subscription
    token=os.getenv("SLACK_BOT_TOKEN"),
    process_before_response=True,  # Required for Lambda
)

# Connect to DynamoDB
dynamodb = boto3.resource("dynamodb")
DYNAMODB_TABLE_NAME = "tmykbot-slack-dev-tab"
table = dynamodb.Table(os.getenv("DYNAMODB_TABLE_NAME", DYNAMODB_TABLE_NAME))


@app.message(re.compile("([a-zA-Z0-9-]+)\+\+"))
def plus_plus_handler(message, say, context):
    for matched_text in context["matches"]:
        try:
            response = table.get_item(Key={"alias": matched_text})

            if (item := response.get("Item")) is None:  # Key does not exist
                total_count = 1
            else:  # Key exists
                total_count = item.get("count", 0) + 1
            table.put_item(
                Item={
                    "alias": matched_text,
                    "count": total_count,
                }
            )
        except Exception as e:
            print(e)
            say("Error:" + e)
            continue

        patterns = (
            f"{matched_text}がプラプラされたよ. ",
            f"{matched_text} いいね!",
            f"{matched_text} ナイス!",
        )
        reply = random.choice(patterns) + f" (++された回数: {total_count})"
        say(reply)


def word_not_found(text, say):
    patterns = (
        f"ごめんね. 「{text}」はわからないよ.",
        f"「{text}」はわからないよ.",
        f"恐れ入りますが「{text}」に関して当方ではわかりかねます.",
    )
    reply = random.choice(patterns)
    say(reply)


@app.message(re.compile("!word ([^ ]+)"))
def word_handler(message, say, context):
    for matched_text in context["matches"]:
        try:
            response = table.get_item(Key={"alias": matched_text})
            if (item := response.get("Item")) is None:  # Key does not exist
                word_not_found(text=matched_text, say=say)
                continue

            # Key exists
            if (desc := item.get("description")) is None:
                word_not_found(text=matched_text, say=say)
                continue

            # Word found
            reply = f"{matched_text}: {desc}"
            say(reply)

        except Exception as e:
            print(e)
            say("Error:" + e)
            continue


if __name__ == "__main__":
    app.start()

# Required for Lambda
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

# Logging for AWS Lambda
SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

# AWS Lambda support
def lambda_handler(event, context):
    slack_handler = SlackRequestHandler(app)
    return slack_handler.handle(event, context)
