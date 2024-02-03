import re
import os
import logging
from slack_bolt import App

logging.basicConfig(level=logging.DEBUG)

# Slack Appの設定
app = App(
    token=os.getenv("SLACK_BOT_TOKEN"),
    signing_secret=os.getenv("SLACK_SIGNING_SECRET"),
    process_before_response=True,
)

# メッセージイベントの処理
@app.message(re.compile("([a-zA-Z0-9-]+)\+\+"))
def handle_message(message, say, context):
    print("Triggered")
    matched_text = context['matches'][0]  # 正規表現にマッチしたテキスト
    say(f"Detected increment for: {matched_text}")

@app.message("hello")
def message_hello(message, say):
    # イベントがトリガーされたチャンネルへ say() でメッセージを送信します
    say(f"Hey there <@{message['user']}>!")

if __name__ == "__main__":
    # python app.py のように実行すると開発用Webサーバーで起動
    # app.start()
    from slack_bolt.adapter.socket_mode import SocketModeHandler
    SocketModeHandler(app, os.getenv("SLACK_APP_TOKEN")).start()

from slack_bolt.adapter.aws_lambda import SlackRequestHandler

# ロギングを AWS Lambda 向けに初期化します
SlackRequestHandler.clear_all_log_handlers()
logging.basicConfig(format="%(asctime)s %(message)s", level=logging.DEBUG)

def lambda_handler(event, context):
    # AWS Lambda用のハンドラーを初期化
    slack_handler = SlackRequestHandler(app)
    # AWS LambdaからのイベントをSlack Bolt Appに渡して処理
    return slack_handler.handle(event, context)
