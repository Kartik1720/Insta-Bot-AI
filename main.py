import time
import undetected_chromedriver as uc
from instagrapi import Client
import openai

# Instagram credentials
USERNAME = "gme955364"
PASSWORD = "Hello@123"

# OpenAI API key
OPENAI_API_KEY = "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"

def generate_reply(message):
    """Generate a reply using OpenAI."""
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )
    return response["choices"][0]["message"]["content"]

def login_instagram():
    """Login to Instagram."""
    client = Client()
    client.login(USERNAME, PASSWORD)
    return client

def check_and_reply(client):
    """Check for unread messages and reply."""
    inbox = client.direct_threads()
    for thread in inbox:
        if thread.messages[0].is_unread:
            sender = thread.messages[0].user_id
            message = thread.messages[0].text
            reply = generate_reply(message)
            client.direct_send(reply, [sender])
            print(f"Replied: {reply}")

def start_bot():
    """Bot lifecycle: check messages every hour, stay online for 5 mins."""
    client = login_instagram()
    while True:
        check_and_reply(client)
        print("Sleeping for 55 minutes...")
        time.sleep(3300)  # 55 minutes
        print("Active for 5 minutes...")

if __name__ == "__main__":
    start_bot()
