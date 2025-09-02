import os
import re
import time
import langchain
from typing import Any
from datetime import timedelta
from dotenv import load_dotenv
from langchain_community.chat_message_histories import MomentoChatMessageHistory
from langchain.schema import HumanMessage, LLMResult, SystemMessage
from langchain.callbacks.base import BaseCallbackHandler
from langchain.schema import LLMResult
from langchain_openai import ChatOpenAI
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler


CHAT_UPDATE_INTERVAL_SEC = 1

load_dotenv()

# LangChainのデバッグを有効化
langchain.debug = True

app = App(
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
    token=os.environ["SLACK_BOT_TOKEN"],
    process_before_response=True,
)

class SlackStreamingCallbackHandler(BaseCallbackHandler):
    last_send_time = time.time()
    message = ""

    def __init__(self, channel, ts):
        self.channel = channel
        self.ts = ts

    def on_llm_new_token(self, token: str, **kwargs) -> None:
        self.message += token

        now = time.time()
        if now - self.last_send_time > CHAT_UPDATE_INTERVAL_SEC:
            self.last_send_time = now
            app.client.chat_update(channel=self.channel, ts=self.ts, text=f"{self.message}...")

    def on_llm_end(self, response: LLMResult, **kwargs: Any) -> Any:
        app.client.chat_update(channel=self.channel, ts=self.ts, text=self.message)

@app.event("app_mention")
def handle_mention(event, say):
    try:
        channel = event["channel"]
        thread_ts = event["ts"]
        message = re.sub("<@.*>", "", event["text"])

        # 投稿のキー(=Momentoキー)：初回=event["ts"],2回目以降=event["thread_ts"]
        id_ts = event["ts"]
        if "thread_ts" in event:
            id_ts = event["thread_ts"]

        result = say("\n\nTyping...", thread_ts=thread_ts)
        ts = result["ts"]

        history = MomentoChatMessageHistory.from_client_params(
            id_ts,
            os.environ["MOMENTO_CACHE"],
            timedelta(hours=int(os.environ["MOMENTO_TTL"])),
        )

        messages = [SystemMessage(content="You are a good assistant.")]
        messages.extend(history.messages)
        messages.append(HumanMessage(content=message))

        history.add_user_message(message)

        callback = SlackStreamingCallbackHandler(channel=channel, ts=ts)
        llm = ChatOpenAI(
            model_name=os.environ["OPENAI_API_MODEL"],
            temperature=float(os.environ["OPENAI_API_TEMPERATURE"]),
            streaming=True,
            callbacks=[callback],
        )

        ai_message = llm.invoke(messages)
        history.add_message(ai_message)
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        say(f"エラーが発生しました: {str(e)}", thread_ts=thread_ts)

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
