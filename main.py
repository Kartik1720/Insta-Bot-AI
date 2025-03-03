from instagrapi import Client, exceptions  # Import exceptions properly
import time
import os
import json
import undetected_chromedriver as uc
from instagrapi import Client
import openai
# No need to import ChallengeChoice

# Instagram credentials
USERNAME = "gme955364"
PASSWORD = "Hello@1234"

# OpenAI API key
OPENAI_API_KEY = "sk-proj-KBB49xKASyzqCYGWz2thZ5IHBzoSZ0kqig4X5tPcqBrJjztz62gS6VT-qnn5v9P6UxY"

SESSION_FILE = "session.json"

def generate_reply(message):
    """Generate a reply using OpenAI."""
    openai.api_key = OPENAI_API_KEY
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": message}]
    )

    return response["choices"][0]["message"]["content"]

def login_instagram():
    """Login to Instagram using session or credentials."""
    client = Client()

    # Use a session file instead of login credentials
    if os.path.exists(SESSION_FILE):
        print("🔄 Loading existing session...")
        try:
            client.load_settings(json.load(open(SESSION_FILE)))
            client.get_timeline_feed()  # Validate session
            print("✅ Session restored successfully!")
            return client
        except Exception as e:
            print(f"⚠️ Error loading session: {e}")
    
    print("⚠️ No valid session found! Log in manually on your local machine first.")
    exit(1)

client = login_instagram()

def handle_challenge(client):
    """Automatically handles Instagram challenge verification"""
    print("⚠️ Challenge Required! Attempting to solve...")
    
    challenge_url = client.last_json.get("challenge", {}).get("url")
    if not challenge_url:
        print("❌ No challenge URL found. Try logging in manually.")
        return False

    # Manually choosing email option
    client.challenge_resolve_simple(challenge_url, choice=1)  # 1 for email

    time.sleep(5)  # Wait for the email from Instagram

    # Ask user to manually check their email and enter the code
    code = input("Enter the 6-digit code sent to your email: ").strip()
    client.challenge_code_apply(code)

    print("✅ Challenge Solved! Login Successful!")
    return True

def check_login_status(client):
    try:
        user_info = client.account_info()
        print(f"✅ Logged in as: {user_info.username} with {user_info.follower_count} followers.")
    except Exception as e:
        print(f"❌ Not logged in! Error: {e}")

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
    # Run locally first to generate session.json
    if not os.path.exists(SESSION_FILE):
        print("⚠️ Running locally to generate session first...")
        login_instagram()
        print("✅ Session saved! Now deploy the bot.")
    else:
        start_bot()
