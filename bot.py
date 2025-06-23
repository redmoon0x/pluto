import os
import telebot
import sqlite3
import json
import requests
from datetime import datetime
from flask import Flask, request

# Initialize Flask app
app = Flask(__name__)

# Initialize bot with token validation
BOT_TOKEN = os.environ.get('BOT_TOKEN')
if not BOT_TOKEN:
    raise ValueError("No BOT_TOKEN environment variable set")
bot = telebot.TeleBot(BOT_TOKEN)

# Database setup
def setup_database():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    # Create settings table for admin configurations
    c.execute('''CREATE TABLE IF NOT EXISTS settings
                (key TEXT PRIMARY KEY, value TEXT)''')
    
    # Create users table for storing user information
    c.execute('''CREATE TABLE IF NOT EXISTS users
                (user_id INTEGER PRIMARY KEY,
                 username TEXT,
                 notes TEXT,
                 last_interaction TIMESTAMP)''')
    
    conn.commit()
    conn.close()

# Load system prompt
def load_system_prompt():
    with open('system_prompt.txt', 'r', encoding='utf-8') as f:
        return f.read()

SYSTEM_PROMPT = load_system_prompt()

# Admin commands
@bot.message_handler(commands=['setapi'])
def set_api_key(message):
    try:
        api_key = message.text.split()[1]
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO settings VALUES (?, ?)", ("api_key", api_key))
        conn.commit()
        conn.close()
        bot.reply_to(message, "API key updated successfully!")
    except:
        bot.reply_to(message, "Usage: /setapi YOUR_API_KEY")

@bot.message_handler(commands=['setbaseurl'])
def set_base_url(message):
    try:
        base_url = message.text.split()[1]
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO settings VALUES (?, ?)", ("base_url", base_url))
        conn.commit()
        conn.close()
        bot.reply_to(message, "Base URL updated successfully!")
    except:
        bot.reply_to(message, "Usage: /setbaseurl YOUR_BASE_URL")

@bot.message_handler(commands=['setmodel'])
def set_model(message):
    try:
        model = message.text.split()[1]
        conn = sqlite3.connect('bot.db')
        c = conn.cursor()
        c.execute("INSERT OR REPLACE INTO settings VALUES (?, ?)", ("model", model))
        conn.commit()
        conn.close()
        bot.reply_to(message, "Model updated successfully!")
    except:
        bot.reply_to(message, "Usage: /setmodel MODEL_NAME")

def get_settings():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    settings = {}
    for key in ['api_key', 'base_url', 'model']:
        c.execute("SELECT value FROM settings WHERE key=?", (key,))
        result = c.fetchone()
        settings[key] = result[0] if result else None
    conn.close()
    return settings

def update_user_info(user_id, username, note):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    
    # Get existing notes
    c.execute("SELECT notes FROM users WHERE user_id=?", (user_id,))
    result = c.fetchone()
    existing_notes = json.loads(result[0]) if result and result[0] else []
    
    # Add new note with timestamp
    new_note = {
        'timestamp': datetime.now().isoformat(),
        'content': note
    }
    existing_notes.append(new_note)
    
    # Update user record
    c.execute('''INSERT OR REPLACE INTO users 
                (user_id, username, notes, last_interaction)
                VALUES (?, ?, ?, ?)''',
                (user_id, username, json.dumps(existing_notes), datetime.now().isoformat()))
    
    conn.commit()
    conn.close()

def get_user_context(user_id):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("SELECT notes FROM users WHERE user_id=?", (user_id,))
    result = c.fetchone()
    conn.close()
    
    if result and result[0]:
        notes = json.loads(result[0])
        return "\n".join([f"- {note['content']}" for note in notes[-5:]])  # Last 5 notes
    return ""

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    settings = get_settings()
    
    if not all(settings.values()):
        bot.reply_to(message, "Bot not configured. Admin needs to set API key, base URL, and model.")
        return
    
    user_context = get_user_context(message.from_user.id)
    
    # Prepare the chat completion request
    headers = {
        'Content-Type': 'application/json',
        'Authorization': f'Bearer {settings["api_key"]}'
    }
    
    data = {
        'model': settings['model'],
        'messages': [
            {'role': 'system', 'content': SYSTEM_PROMPT},
            {'role': 'system', 'content': f"User context:\n{user_context}"},
            {'role': 'user', 'content': message.text}
        ]
    }
    
    try:
        response = requests.post(
            f"{settings['base_url']}/v1/chat/completions",
            headers=headers,
            json=data
        )
        
        if response.status_code == 200:
            bot_response = response.json()['choices'][0]['message']['content']
            bot.reply_to(message, bot_response)
            
            # Update user info with the interaction
            update_user_info(
                message.from_user.id,
                message.from_user.username,
                f"User said: {message.text}\nBot responded: {bot_response}"
            )
        else:
            bot.reply_to(message, "Sorry, I'm having trouble thinking right now...")
            
    except Exception as e:
        bot.reply_to(message, "Sorry, I'm having trouble connecting to my brain...")
        print(f"Error: {e}")

# Webhook route
@app.route('/' + BOT_TOKEN, methods=['POST'])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return ''

# Health check route
@app.route('/')
def health():
    return 'Bot is running!'

if __name__ == "__main__":
    setup_database()
    print("Bot started...")
    # No auto webhook setup - managed through Gradio interface
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))
