SLACK_BOT_TOKEN = ""
SLACK_APP_TOKEN = ""

API_TYPE = ""
API_BASE = ""
API_VERSION = ""
API_KEY = ""

import os
import openai

from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack import WebClient
from slack_bolt import App

app = App(token=SLACK_BOT_TOKEN)
client = WebClient(SLACK_BOT_TOKEN)

@app.event("app_mention")
def handle_message_events(body, logger):
    print(str(body["event"]["text"]).split(">")[1])

    prompt = str(body["event"]["text"]).split(">")[1]

    response = client.chat_postMessage(channel=body["event"]["channel"],
                                       thread_ts=body["event"]["event_ts"],
                                       text=f"Hello from your ScoutBot! :robot_face: \nThanks for your request, I will try to answer it as soon as possible!")

    openai.api_type = API_TYPE
    openai.api_base = API_BASE
    openai.api_version = API_VERSION
    openai.api_key = API_KEY

    response = openai.ChatCompletion.create(
        engine="demo-ai",
        messages = [
            {"role":"user", "content":prompt}
            ],
        temperature=0.5,
        max_tokens=500,
        top_p=0.95,
        frequency_penalty=0,
        presence_penalty=0,
        stop=None
        ).choices[0]["message"]["content"]

    response = client.chat_postMessage(channel=body["event"]["channel"],
                                       thread_ts=body["event"]["event_ts"],
                                       text=f"Here you go: \n{response}")


if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
