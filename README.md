# Telegram AI Chatbot with Custom LLM Support

A Telegram bot that can connect to OpenAI-compatible APIs (like LocalAI, text-generation-webui) with customizable settings and user context memory.

## Features

- Compatible with OpenAI-style API endpoints
- Configurable base URL, model name, and API key
- Stores user interaction history for context
- Uses custom system prompt for bot personality
- SQLite database for persistent storage
- Web interface for configuration and monitoring
- Easy deployment to Hugging Face Spaces

## Local Setup

1. Create a Telegram bot:
   - Message @BotFather on Telegram
   - Use `/newbot` command and follow instructions
   - Save the bot token

2. Clone this repository and install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set environment variables:
   ```bash
   export BOT_TOKEN="your_bot_token_here"
   ```

4. Run the application:
   ```bash
   python app.py
   ```

5. Access the control panel at http://localhost:7860

## Deploy to Hugging Face Space

1. Create a new Space:
   - Visit huggingface.co/spaces
   - Click "Create new Space"
   - Select "Gradio" as the SDK
   - Choose Python 3.9+ as the runtime

2. Upload Files:
   - Upload all project files to the Space
   - Make sure to include:
     - app.py (main entry point)
     - bot.py (bot logic)
     - system_prompt.txt (bot personality)
     - requirements.txt (dependencies)

3. Configure Environment Variables:
   In your Space's Settings > Repository secrets, add:
   - BOT_TOKEN: Your Telegram bot token

4. Set Up Webhook:
   After deployment:
   1. Visit your Space's URL to access the control panel
   2. Go to "Configuration" tab
   3. Enter webhook URL: `https://your-space-name.hf.space/webhook`
   4. Click "Start Bot"
   5. Configure API settings for your LLM provider

## Control Panel Features

### Configuration Tab
- Set webhook URL and start bot
- Configure API settings:
  - API Key
  - Base URL
  - Model Name

### Monitoring Tab
- View current bot settings
- Monitor user statistics
- Check bot status

### Database Management Tab
- Clear user interaction data
- Clear bot settings
- Reset entire database
- Safety warnings for destructive actions

## Architecture

- `app.py`: Web interface and control panel
- `bot.py`: Telegram bot implementation
- `system_prompt.txt`: Bot personality definition
- `bot.db`: SQLite database (auto-created) storing:
  - User interaction history
  - Bot configurations
  - Admin settings

## Notes

- The bot stores the last 5 interactions per user for context
- Each message updates the user's interaction history
- System prompt defines the bot's personality and behavior
- Settings can be updated through the web interface
- Database is automatically initialized on startup

## Requirements

- Python 3.9+
- Telegram Bot Token
- OpenAI-compatible API endpoint
