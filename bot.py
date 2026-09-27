import os
import threading
from flask import Flask
from telethon import TelegramClient, events
import tweepy

# ==========================================
# FLASK
# ==========================================

app = Flask(__name__)

@app.route("/")
def home():
    return "Telegram to X/Twitter Bot is running 24/7!"


# ==========================================
# TELEGRAM SETTINGS
# ==========================================

api_id = 37007922
api_hash = "06daa70876742419f268ffaadc42a251"

# আপনার Source Telegram Channel
CHANNEL_USERNAME = os.environ.get(
    "CHANNEL_USERNAME",
    "@MiddleEastEnglis"
)

SESSION_NAME = "bot_session"


# ==========================================
# X / TWITTER INFORMATION
# ==========================================

CONSUMER_KEY = "TXhmAs92dypvAVE9Qtxpzcc00"
CONSUMER_SECRET = "gm8uxcKtXpYo6hmQkyW5NTMs00khKIw4E UToSJdvAraJYciTdP"

ACCESS_TOKEN = "2101239653470973952-KfS9LGmHvhv2eAXNjIzvH75Kd7X1zi"
ACCESS_TOKEN_SECRET = "PTIIv4AJHc3vnvgU7KTKUt2ZPBYC55BEGxVxNfXMZzDVz"


# ==========================================
# TELEGRAM CLIENT
# ==========================================

client = TelegramClient(
    SESSION_NAME,
    api_id,
    api_hash
)


# ==========================================
# X / TWITTER CLIENT
# ==========================================

twitter_client = tweepy.Client(
    consumer_key=CONSUMER_KEY,
    consumer_secret=CONSUMER_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)


# ==========================================
# HASHTAGS
# ==========================================

def generate_tags(text):
    text_lower = text.lower()
    tags = ["#MiddleEast", "#News"]

    if any(word in text_lower for word in [
        "war", "conflict", "attack", "military",
        "army", "fighting", "strike", "missile"
    ]):
        tags.append("#MiddleEastConflict")

    if any(word in text_lower for word in [
        "economy", "oil", "gas", "market",
        "trade", "dollar"
    ]):
        tags.append("#Economy")

    if any(word in text_lower for word in [
        "palestine", "gaza", "israel", "lebanon",
        "iran", "dubai", "saudi"
    ]):
        tags.append("#BreakingNews")

    return " ".join(tags)


# ==========================================
# NEW TELEGRAM NEWS LISTENER
# ==========================================

@client.on(events.NewMessage(chats=CHANNEL_USERNAME))
async def news_handler(event):
    print("====================================")
    print("NEW TELEGRAM NEWS RECEIVED")
    print("====================================")

    news_text = event.raw_text.strip()

    if not news_text:
        print("No text. Skipping.")
        return

    try:
        tags = generate_tags(news_text)
        telegram_link = "https://t.me/+9bvReXpQo_szMGM1"

        extra_text = (
            f"\n\n{tags}"
            f"\n\nSubscribe for more updates:"
            f"\n{telegram_link}"
        )

        # X maximum 280 characters limit
        allowed_length = 280 - len(extra_text)

        final_tweet = (
            news_text[:allowed_length].rstrip()
            + extra_text
        )

        print("Posting to X...")
        result = twitter_client.create_tweet(text=final_tweet)
        print("SUCCESS! Tweet ID:", result.data["id"])

    except Exception as e:
        print("X/TWITTER ERROR:", str(e))


# ==========================================
# TELEGRAM RUNNER
# ==========================================

def run_telegram():
    try:
        print("Starting Telegram...")
        client.start()
        print("Telegram connected! Watching:", CHANNEL_USERNAME)
        client.run_until_disconnected()
    except Exception as e:
        print("TELEGRAM ERROR:", str(e))


# ==========================================
# START APP & BOT
# ==========================================

if __name__ == "__main__":
    telegram_thread = threading.Thread(
        target=run_telegram,
        daemon=True
    )
    telegram_thread.start()

    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
