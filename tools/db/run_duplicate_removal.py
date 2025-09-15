import sys
import os

# Add the server directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'server')))

from db_utils import Database
import config

def run_duplicate_removal():
    print("Connecting to database...")
    db = Database(config.DB_CONFIG)
    print("Database connection established. Removing duplicates...")
    try:
        db.remove_duplicates()
        print("Duplicate removal process completed.")
    except Exception as e:
        print(f"An error occurred during duplicate removal: {e}")

if __name__ == "__main__":
    run_duplicate_removal()
