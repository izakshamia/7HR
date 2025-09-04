import argparse
import json
import os
import time
import requests
import config
from card_utils import format_card
from db_utils import Database

class Bot:
    def __init__(self, db):
        self.db = db

    def send_card(self, message):
        url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
        resp = requests.post(url, data={
            "chat_id": config.TELEGRAM_CHAT_ID,
            "text": message,
            "parse_mode": "Markdown"
        })
        if not resp.ok:
            print(f"Failed to send message: {resp.text}")

    def load_last_sent_id(self):
        if os.path.exists(config.TRACK_FILE):
            with open(config.TRACK_FILE, "r") as f:
                return json.load(f).get("last_id", 0)
        return 0

    def save_last_sent_id(self, last_id):
        with open(config.TRACK_FILE, "w") as f:
            json.dump({"last_id": last_id}, f)

    def poll_new_candidates(self):
        print(f"Polling every {config.POLL_INTERVAL} seconds for new candidates...")
        last_sent_id = self.load_last_sent_id()
        sent_ids = set()
        while True:
            try:
                rows = self.db.fetch_new_candidates(last_sent_id)
                for row in rows:
                    row_id, data = row
                    data["id"] = row_id  # Attach DB row id for correct More Info link
                    if row_id in sent_ids:
                        continue  # Already sent in this session
                    card = format_card(data)
                    print(f"Sending candidate {row_id}: {card}")
                    self.send_card(card)
                    sent_ids.add(row_id)
                    last_sent_id = row_id
                    self.save_last_sent_id(last_sent_id)
            except Exception as e:
                print(f"Error during polling: {e}")
            time.sleep(config.POLL_INTERVAL)

    def send_all_candidates(self, limit=10):
        print(f"Sending all candidates (limit: {limit})...")
        try:
            rows = self.db.fetch_all_candidates(limit=limit)
            for row in rows:
                row_id, data = row
                data["id"] = row_id
                card = format_card(data)
                print(f"Sending candidate {row_id}: {card}")
                self.send_card(card)
        except Exception as e:
            print(f"Error sending all candidates: {e}")

def main():
    parser = argparse.ArgumentParser(description="Telegram CV Bot")
    parser.add_argument("--poll", action="store_true", help="Poll for new candidates and send them to Telegram.")
    parser.add_argument("--send-all", action="store_true", help="Send all candidates to Telegram.")
    parser.add_argument("--limit", type=int, default=10, help="Limit the number of candidates to send with --send-all.")
    args = parser.parse_args()

    db = Database(config.DB_CONFIG)
    bot = Bot(db)

    if args.poll:
        if config.AUTO_SEND_ENABLED:
            print("[AutoSend] AUTO_SEND_ENABLED is true. Starting polling...")
            bot.poll_new_candidates()
        else:
            print("[AutoSend] AUTO_SEND_ENABLED is not set to true. Exiting.")
    elif args.send_all:
        bot.send_all_candidates(limit=args.limit)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
