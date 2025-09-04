# Project Overview

This project is a Telegram bot that retrieves candidate CVs from a PostgreSQL database and sends them to a specified Telegram chat. It also provides a web interface to view more details about each candidate.

The project has a polyglot architecture, using both Python and Node.js.

*   **Python:**
    *   The core bot logic is in `server/bot.py`. It polls the database for new candidates and sends them to Telegram.
    *   A Flask web server (`server/card_info_server.py`) provides a web UI to view candidate details.
    *   `server/db_utils.py` handles all interactions with the PostgreSQL database.
    *   `server/card_utils.py` formats the candidate data into a Markdown card for Telegram.
    *   `server/config.py` manages the project's configuration, pulling values from a `.env` file.

*   **Node.js:**
    *   `package.json` manages the project's dependencies. Although the core logic is in Python, Node.js is used for dependency management.

# Building and Running

## Dependencies

1.  **Node.js:** Install Node.js dependencies with `npm install`.
2.  **Python:** Install Python dependencies with `pip install -r requirements.txt`.  **TODO:** A `requirements.txt` file is missing. You can create one based on the imports in the Python files (e.g., `requests`, `psycopg2-binary`, `Flask`, `python-dotenv`).

## Configuration

1.  Create a `.env` file in the root of the project.
2.  Add the following environment variables to the `.env` file:
    *   `TELEGRAM_BOT_TOKEN`: Your Telegram bot token.
    *   `TELEGRAM_CHAT_ID`: The ID of the Telegram chat to send messages to.
    *   `DB_HOST`: The hostname of your PostgreSQL database.
    *   `DB_PORT`: The port of your PostgreSQL database.
    *   `DB_NAME`: The name of your PostgreSQL database.
    *   `DB_USER`: The username for your PostgreSQL database.
    *   `DB_PASSWORD`: The password for your PostgreSQL database.
    *   `POLL_INTERVAL`: The interval in seconds to poll for new candidates (e.g., `60`).
    *   `AUTO_SEND_ENABLED`: Set to `true` to automatically send new candidates.
    *   `UPLOAD_DIR`: The directory to store uploaded files.

## Running the Application

1.  **Start the Web Server:**
    ```bash
    python server/card_info_server.py
    ```
    This will start the Flask web server on `http://localhost:5001`.

2.  **Run the Bot:**
    *   To poll for new candidates:
        ```bash
        python server/bot.py --poll
        ```
    *   To send all candidates (up to a limit of 10 by default):
        ```bash
        python server/bot.py --send-all --limit 20
        ```

# Development Conventions

*   **Configuration:** All configuration is managed through environment variables loaded from a `.env` file.
*   **Database:** The project uses a PostgreSQL database. All database logic is contained in `server/db_utils.py`.
*   **Telegram Bot:** The Telegram bot logic is in `server/bot.py`.
*   **Web Interface:** A Flask web server provides a web interface to view candidate details.
