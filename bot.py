import os
import re
from flask import Flask
from telethon import TelegramClient, events
import tweepy

# ফ্লাস্ক সার্ভার (রেন্ডারে ২৪ ঘণ্টা সচল রাখার জন্য)
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram to Twitter Bot with Auto Tags is running 24/7!"

# টেলিগ্রাম এবং টুইটার তথ্য
api_id = 33811130
api_hash = '35c54c9092e2a2927cdbcc8be0208b84'

# আপনার সোর্স টেলিগ্রাম চ্যানেল
channel_username = '@MiddleEastEnglis'  

# আপনার টুইটার ডেভেলপার অ্যাকাউন্ট থেকে পাওয়া সঠিক API Keys এবং Tokens এখানে বসানো হলো
consumer_key = "zfMy1BjfcwoppZgnnNm0xS4ka"
consumer_secret = "m1TrppKqKXBM4zHINXxf2IrqLX7fc5eJyrb09dvBqo85UKSuvI"
access_token = "2101239653470973952-rwitUkKRFKXe9b5iTRghuFZrgPwPd2"
access_token_secret = "KB9WCCg8HFFmiwp3b1sexWVsbg2Rmxq3L9f8i95e2YjY4"

# টুইটার ক্লায়েন্ট সেটআপ
twitter_client = tweepy.Client(
    consumer_key=consumer_key,
    consumer_secret=consumer_secret,
    access_token=access_token,
    access_token_secret=access_token_secret
)

# টেলিগ্রাম ক্লায়েন্ট ইনিশিয়ালাইজ (Termux থেকে তৈরি session_name ব্যবহার করবে)
client = TelegramClient('session_name', api_id, api_hash)

# নিউজ বা টেক্সট থেকে ক্যাটাগরি অনুযায়ী হ্যাশট্যাগ জেনারেট করার ফাংশন
def generate_tags(text):
    text_lower = text.lower()
    tags = ["#MiddleEast", "#News"]
    
    if any(word in text_lower for word in ['war', 'conflict', 'attack', 'military', 'army', 'fighting']):
        tags.append("#MiddleEastConflict")
    if any(word in text_lower for word in ['economy', 'oil', 'gas', 'market', 'trade', 'dollar']):
        tags.append("#Economy")
    if any(word in text_lower for word in ['palestine', 'gaza', 'israel', 'lebanon', 'iran', 'dubai', 'saudi']):
        tags.append("#BreakingNews")
        
    return " ".join(tags)

@client.on(events.NewMessage(chats=channel_username))
async def my_event_handler(event):
    news_text = event.raw_text
    if news_text:
        try:
            # ক্যাটাগরি অনুযায়ী হ্যাশট্যাগ তৈরি
            auto_tags = generate_tags(news_text)
            
            # সাবস্ক্রাইব মেসেজ এবং আপনার টেলিগ্রাম লিংক
            telegram_link = "https://t.me/+9bvReXpQo_szMGM1"
            subscribe_text = f"\n\n{auto_tags}\n\nSubscribe for more updates:\n{telegram_link}"
            
            # টুইটারের ২৮০ ক্যারেক্টার লিমিট ঠিক রেখে নিউজ, ট্যাগ ও লিংক অ্যাডজাস্ট করা
            allowed_news_length = 280 - len(subscribe_text)
            final_tweet = news_text[:allowed_news_length] + subscribe_text

            # টুইটারে পোস্ট করা
            twitter_client.create_tweet(text=final_tweet)
            print("News posted to Twitter with tags and Telegram link successfully!")
        except Exception as e:
            print(f"Error posting to Twitter: {e}")

if __name__ == '__main__':
    import threading
    def run_telegram_bot():
        client.start()
        client.run_until_disconnected()

    t = threading.Thread(target=run_telegram_bot)
    t.start()

    # রেন্ডারের জন্য পোর্ট সেটআপ
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)
