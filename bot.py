import os
import threading
from flask import Flask
from telethon import TelegramClient, events
import tweepy

# ==========================================
# FLASK SERVER
# ==========================================

app = Flask(__name__)

@app.route("/")
def home():
    return "Telegram to X/Twitter Bot is running 24/7!"


# ==========================================
# TELEGRAM SETTINGS
# ==========================================
# ==========================================
# TELEGRAM SETTINGS
# ==========================================

api_id = 137007922
api_hash = "06daa70876742419f268ffaadc42a25"



# আপনার Source Telegram Channel
CHANNEL_USERNAME = os.environ.get(
    "CHANNEL_USERNAME",
    "@MiddleEastEnglis"
)

# Telethon session file
SESSION_NAME = os.environ.get(
    "SESSION_NAME",
    "session_name"
)


# ==========================================
# X / TWITTER SETTINGS
# ==========================================

consumer_key =G364SBW0l5n0kSdGf3omZawf7 os.environ["TW_CONSUMER_KEY"]
consumer_secret =nNGU6u3nraU95ZBepck0krhIl5xCJy3EkEGSIsu35hhJWdWZUq os.environ["TW_CONSUMER_SECRET"]
access_token =2101239653470973952-YEJ0qfHXMFFW5gEcVaaJ5Qa5vWTz1v os.environ["TW_ACCESS_TOKEN"]
access_token_secret =pE2nfVxtJBdZlV8QkIn1hO5vRHHce5pGLUMmlTYgptliC os.environ["TW_ACCESS_TOKEN_SECRET"]


# X/Twitter client
twitter_client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)


# ==========================================
# TELEGRAM CLIENT
# ==========================================

client = TelegramClient(
    SESSION_NAME,
    api_id,
    api_hash
)


# ==========================================
# AUTO HASHTAGS
# ==========================================

def generate_tags(text):

    text_lower = text.lower()

    tags = [
        "#MiddleEast",
        "#News"
    ]

    if any(word in text_lower for word in [
        "war",
        "conflict",
        "attack",
        "military",
        "army",
        "fighting",
        "strike",
        "missile"
    ]):
        tags.append("#MiddleEastConflict")

    if any(word in text_lower for word in [
        "economy",
        "oil",
        "gas",
        "market",
        "trade",
        "dollar"
    ]):
        tags.append("#Economy")

    if any(word in text_lower for word in [
        "palestine",
        "gaza",
        "israel",
        "lebanon",
        "iran",
        "dubai",
        "saudi"
    ]):
        tags.append("#BreakingNews")

    return " ".join(tags)


# ==========================================
# TELEGRAM NEW MESSAGE
# ==========================================

@client.on(events.NewMessage(chats=CHANNEL_USERNAME))
async def my_event_handler(event):

    print("=" * 50)
    print("NEW TELEGRAM NEWS RECEIVED")
    print("=" * 50)

    news_text = event.raw_text.strip()

    print("News:")
    print(news_text[:500])

    if not news_text:
        print("No text found. Skipping.")
        return

    try:

        # Generate hashtags
        auto_tags = generate_tags(news_text)

        # Telegram channel link
        telegram_link = os.environ.get(
            "TELEGRAM_LINK",
            "https://t.me/+9bvReXpQo_szMGM1"
        )

        subscribe_text = (
            f"\n\n{auto_tags}"
            f"\n\nSubscribe for more updates:"
            f"\n{telegram_link}"
        )

        # X limit
        allowed_news_length = 280 - len(subscribe_text)

        if allowed_news_length < 1:
            print("Error: Tags/link are too long.")
            return

        final_tweet = (
            news_text[:allowed_news_length].rstrip()
            + subscribe_text
        )

        print("=" * 50)
        print("POSTING TO X/TWITTER")
        print("=" * 50)
        print(final_tweet)

        # Post tweet
        response = twitter_client.create_tweet(
            text=final_tweet
        )

        print("SUCCESS!")
        print("Tweet ID:", response.data["id"])

    except Exception as e:

        print("=" * 50)
        print("ERROR POSTING TO X/TWITTER")
        print("=" * 50)
        print(type(e).__name__)
        print(str(e))


# ==========================================
# TELEGRAM BOT
# ==========================================

def run_telegram_bot():

    try:

        print("=" * 50)
        print("STARTING TELEGRAM CLIENT")
        print("=" * 50)

        client.start()

        print("Telegram client started successfully.")
        print("Listening to:", CHANNEL_USERNAME)

        client.run_until_disconnected()

    except Exception as e:

        print("=" * 50)
        print("TELEGRAM ERROR")
        print("=" * 50)
        print(type(e).__name__)
        print(str(e))


# ==========================================
# MAIN
# ==========================================

if __name__ == "__main__":

    # Start Telegram in background
    telegram_thread = threading.Thread(
        target=run_telegram_bot,
        daemon=True
    )

    telegram_thread.start()

    # Render port
    port = int(
        os.environ.get("PORT", 5000)
    )

    print("=" * 50)
    print("FLASK SERVER STARTING")
    print("PORT:", port)
    print("=" * 50)

    app.run(
        host="0.0.0.0",
        port=port
    )
