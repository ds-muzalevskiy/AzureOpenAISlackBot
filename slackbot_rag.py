SLACK_BOT_TOKEN = ""
SLACK_APP_TOKEN = ""

AZURE_ENDPOINT = ""
API_VERSION = ""
API_KEY = ""

import os
import openai

from slack_bolt.adapter.socket_mode import SocketModeHandler
from slack import WebClient
from slack_bolt import App

from llama_index.llms.azure_openai import AzureOpenAI
from llama_index.embeddings.azure_openai import AzureOpenAIEmbedding
from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.core import Settings

app = App(token=SLACK_BOT_TOKEN)
client = WebClient(SLACK_BOT_TOKEN)

@app.event("app_mention")
def handle_message_events(body, logger):
    try:
        print(str(body["event"]["text"]).split(">")[1])
    
        prompt = str(body["event"]["text"]).split(">")[1]
    
        response = client.chat_postMessage(channel=body["event"]["channel"],
                                           thread_ts=body["event"]["event_ts"],
                                           text=f"Hello from your ScoutBot! :robot_face: \nThanks for your request, I will try to answer it as soon as possible!")
    
        llm = AzureOpenAI(
        model="gpt-35-turbo",
        deployment_name="demo-ai",
        api_key=API_KEY,
        azure_endpoint=AZURE_ENDPOINT,
        api_version=API_VERSION)
    
    
        embed_model = AzureOpenAIEmbedding(
        model="text-embedding-ada-002",
        deployment_name="SlackEmbedding",
        api_key=API_KEY,
        azure_endpoint=AZURE_ENDPOINT,
        api_version=API_VERSION)
    
        Settings.llm = llm
        Settings.embed_model = embed_model
    
        documents = SimpleDirectoryReader('data').load_data()
        index = VectorStoreIndex.from_documents(documents)
        
        query_engine = index.as_query_engine()
        response = query_engine.query(prompt)
    
        response = client.chat_postMessage(channel=body["event"]["channel"],
                                           thread_ts=body["event"]["event_ts"],
                                           text=f"Here you go: \n{response}")
    except Exception as e:
        logger.error(f"Error handling message: {e}")
        client.chat_postMessage(
            channel=body["event"]["channel"],
            thread_ts=body["event"]["event_ts"],
            text="Oops! Something went wrong while processing your request."
        )

if __name__ == "__main__":
    SocketModeHandler(app, SLACK_APP_TOKEN).start()
