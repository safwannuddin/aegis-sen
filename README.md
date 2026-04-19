# Aegis-Sen

A Discord bot that acts as a bridge between Gemini AI and Discord, allowing you to chat with Gemini directly in your server.

## Features

- **Real-time Chat**: Talk to Gemini in any text channel.
- **Slash Commands**: Easy-to-use commands for bot management.
- **Environment Config**: Secure API key management using `.env`.

## Prerequisites

- **Python 3.8+**
- **A Discord Bot Token** (from [Discord Developer Portal](https://discord.com/developers/applications))
- **A Gemini API Key** (from [Google AI Studio](https://aistudio.google.com/))

## Installation

1.  **Clone the repository** (or download the source code).

2.  **Create a virtual environment** (recommended):
    ```bash
    python -m venv venv
    ```

3.  **Activate the virtual environment**:
    - Windows:
      ```bash
      .\venv\Scripts\activate
      ```
    - Linux/Mac:
      ```bash
      source venv/bin/activate
      ```

4.  **Install dependencies**:
    ```bash
    pip install "fastapi[standard]" requests google-generativeai discord.py python-dotenv
    ```

5.  **Configure Environment Variables**:
    Create a `.env` file in the same directory as `main.py` and add your credentials:

    ```env
    DISCORD_BOT_TOKEN=your_discord_bot_token_here
    GEMINI_API_KEY=your_gemini_api_key_here
    ```

## Usage

Run the bot using Python:

```bash
python main.py
```

## Discord Commands

Once the bot is running and added to your server, you can use the following slash commands:

- `/chat [message]`: Send a message to Gemini.
- `/help`: Display bot information and commands.
- `/ping`: Check if the bot is online.