# Telegram AI Chatbot with Custom LLM Support

A Telegram bot that can connect to OpenAI-compatible APIs (like LocalAI, text-generation-webui) with customizable settings and user context memory.

## Features

- Compatible with OpenAI-style API endpoints
- Configurable base URL, model name, and API key
- Stores user interaction history for context
- Uses custom system prompt for bot personality
- SQLite database for persistent storage
- Easy deployment to Render

## Setup

1. Create a Telegram bot:
   - Message @BotFather on Telegram
   - Use `/newbot` command and follow instructions
   - Save the bot token

2. Clone this repository and update `bot.py`:
   ```python
   BOT_TOKEN = "your_bot_token_here"
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run the bot:
   ```bash
   python bot.py
   ```

## Admin Commands

Configure the bot using these Telegram commands:

- `/setapi YOUR_API_KEY` - Set the API key for your LLM provider
- `/setbaseurl YOUR_BASE_URL` - Set the base URL (e.g., http://localhost:8080)
- `/setmodel MODEL_NAME` - Set the model name to use

## Deploy to Render

1. Create a new Web Service on Render
2. Connect your repository
3. Configure:
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `gunicorn bot:app`
4. Add Environment Variables:
   - `BOT_TOKEN`: Your Telegram bot token
   - `WEBHOOK_URL`: https://your-app.onrender.com/YOUR_BOT_TOKEN
   - `PORT`: 8080 (or let Render set it automatically)

After deployment:
1. Visit your app URL to verify it's running (you should see "Bot is running!")
2. The bot will automatically set up the webhook on startup
3. Configure the bot using admin commands in Telegram

## Architecture

- `bot.py`: Main bot code
- `system_prompt.txt`: Bot personality definition
- `bot.db`: SQLite database (auto-created) storing:
  - User interaction history
  - Bot configurations
  - Admin settings

## Notes

- The bot stores the last 5 interactions per user for context
- Each message updates the user's interaction history
- System prompt defines the bot's personality and behavior
- Bot requires admin configuration before first use

## Requirements

- Python 3.7+
- Telegram Bot Token
- OpenAI-compatible API endpoint
