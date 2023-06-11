import slack
import os
from pathlib import Path
from dotenv import load_dotenv
from flask import Flask
from slackeventsapi import SlackEventAdapter
from llm import *
import time


env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)

app = Flask(__name__)
slack_event_adaptor = SlackEventAdapter(
    os.environ['SIGNIN_SECRET'],
    '/slack/events',
    app
)


client = slack.WebClient(token=os.environ['SLACK_TOKEN'])
BOT_ID = client.api_call("auth.test")['user_id']

# # post a message
# client.chat_postMessage(channel="#bot",
#                         text="oi it's james innit",
#                         icon_url="https://yt3.googleusercontent.com/ytc/AGIKgqM5dw5ZVAuz4UkSPxoKSqagE17Q1pj4zkGPS9L3=s900-c-k-c0x00ffffff-no-rj")
# # client.conversations_list()


@slack_event_adaptor.on("message")
def message(payload):
    event = payload.get('event', {})

    prev_is_user = True if 'user' in event.keys() else False

    if prev_is_user:
        query = event.get('text')
        query = query.strip()+'?' if '?' not in query else query

        ans = qa_pipeline(query, n_responses=1)

        client.chat_postMessage(channel="#hoffbot-demo",
                                text=ans,
                                icon_url="https://yt3.googleusercontent.com/ytc/AGIKgqM5dw5ZVAuz4UkSPxoKSqagE17Q1pj4zkGPS9L3=s900-c-k-c0x00ffffff-no-rj")


if __name__ == "__main__":
    app.run(debug=True, port=8880)


# how long does the bloom period take in pour over
# what is the ratio of coffee grounds to water in the v60
# how long does the chemex take
# how hot can i steam milk before ruining it
# what is a good travel brewer
