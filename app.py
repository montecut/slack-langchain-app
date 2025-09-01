import os
import re

from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import langchain

load_dotenv()

# LangChainのデバッグを有効化（必要時はTrueに変更）
langchain.debug = False

app = App(
    token=os.environ["SLACK_BOT_TOKEN"]
)

@app.event("app_mention")
def handle_mention(event, say):
    thread_ts = event["ts"]
    message = re.sub("<@.*>", "", event["text"])

    llm = ChatOpenAI(
        model_name=os.environ["OPENAI_API_MODEL"],
        temperature=float(os.environ["OPENAI_API_TEMPERATURE"]),
    )

    response = llm.invoke(message)
    say(thread_ts=thread_ts, text=response.content)

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
