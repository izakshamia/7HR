import os
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

PORT = int(os.getenv("PORT", 3000))
NODE_ENV = os.getenv("NODE_ENV", "development")

DB_CONFIG = {
    "host": os.getenv("DB_HOST"),
    "port": int(os.getenv("DB_PORT", 5432)),
    "dbname": os.getenv("DB_NAME"),
    "user": os.getenv("DB_USER"),
    "password": os.getenv("DB_PASSWORD")
}

POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", 60))
AUTO_SEND_ENABLED = os.getenv("AUTO_SEND_ENABLED", "false").lower() == "true"

UPLOAD_DIR = os.getenv("UPLOAD_DIR", "./uploads")

TRACK_FILE = os.path.join(os.path.dirname(__file__), "last_sent_id.json")
