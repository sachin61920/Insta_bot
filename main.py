
import os
import time
import random
from instagrapi import Client
from dotenv import load_dotenv
from keep_alive import keep_alive

keep_alive()

load_dotenv()

USERNAME = os.getenv("IG_USERNAME")
PASSWORD = os.getenv("IG_PASSWORD")

cl = Client()
cl.login(USERNAME, PASSWORD)

replied_messages = set()
active = True

def load_messages():
    with open("messages.txt", "r", encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]

def main_loop():
    global active
    messages = load_messages()
    print("Bot is running...")
    while True:
        threads = cl.direct_threads(amount=10)
        for thread in threads:
            if not thread.users or not thread.items:
                continue
            last_msg = thread.items[0]
            msg_id = last_msg.id
            user_id = last_msg.user_id

            if msg_id in replied_messages:
                continue

            text = last_msg.text.lower()

            if text == "!stop":
                active = False
                cl.direct_send("✅ Bot stopped.", thread.id)
                replied_messages.add(msg_id)
                continue
            elif text == "!start":
                active = True
                cl.direct_send("🚀 Bot started.", thread.id)
                replied_messages.add(msg_id)
                continue

            if active and user_id != cl.user_id:
                reply = random.choice(messages)
                cl.direct_send(reply, thread.id)
                replied_messages.add(msg_id)
                time.sleep(random.uniform(1.5, 3.5))
        time.sleep(5)

if __name__ == "__main__":
    main_loop()
