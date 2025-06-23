import os
import gradio as gr
import sqlite3
from bot import bot, app, setup_database
import threading
import json
from datetime import datetime

def initialize_db():
    setup_database()
    return "Database initialized successfully!"

def update_setting(key, value):
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("INSERT OR REPLACE INTO settings VALUES (?, ?)", (key, value))
    conn.commit()
    conn.close()
    return f"{key} updated successfully!"

def view_settings():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("SELECT * FROM settings")
    settings = dict(c.fetchall())
    conn.close()
    return json.dumps(settings, indent=2)

def view_users():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("SELECT user_id, username, last_interaction FROM users")
    users = c.fetchall()
    conn.close()
    
    if not users:
        return "No users found"
    
    result = "Users:\n"
    for user_id, username, last_interaction in users:
        result += f"ID: {user_id}, Username: {username}, Last active: {last_interaction}\n"
    return result

def clear_user_data():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("DELETE FROM users")
    conn.commit()
    conn.close()
    return "All user data has been cleared!"

def clear_settings():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("DELETE FROM settings")
    conn.commit()
    conn.close()
    return "All settings have been cleared!"

def clear_all_data():
    conn = sqlite3.connect('bot.db')
    c = conn.cursor()
    c.execute("DELETE FROM users")
    c.execute("DELETE FROM settings")
    conn.commit()
    conn.close()
    return "All database data has been cleared!"

def start_bot(webhook_url):
    if not webhook_url:
        return "Please provide a webhook URL"
    
    try:
        # Remove and set new webhook
        bot.remove_webhook()
        bot.set_webhook(webhook_url)
        return f"Webhook set to: {webhook_url}"
    except Exception as e:
        return f"Error setting webhook: {str(e)}"

# Create Gradio interface
def create_interface():
    with gr.Blocks(title="Telegram AI Bot Control Panel") as interface:
        gr.Markdown("# Telegram AI Bot Control Panel")
        
        with gr.Tab("Configuration"):
            with gr.Group():
                gr.Markdown("## Bot Settings")
                webhook_url = gr.Textbox(label="Webhook URL")
                start_btn = gr.Button("Start Bot")
                start_output = gr.Textbox(label="Start Status")
                start_btn.click(start_bot, inputs=[webhook_url], outputs=[start_output])
            
            with gr.Group():
                gr.Markdown("## API Settings")
                api_key = gr.Textbox(label="API Key", type="password")
                base_url = gr.Textbox(label="Base URL")
                model = gr.Textbox(label="Model Name")
                
                api_btn = gr.Button("Update API Key")
                url_btn = gr.Button("Update Base URL")
                model_btn = gr.Button("Update Model")
                
                settings_output = gr.Textbox(label="Settings Status")
                
                api_btn.click(update_setting, inputs=[gr.Textbox(value="api_key", visible=False), api_key], outputs=[settings_output])
                url_btn.click(update_setting, inputs=[gr.Textbox(value="base_url", visible=False), base_url], outputs=[settings_output])
                model_btn.click(update_setting, inputs=[gr.Textbox(value="model", visible=False), model], outputs=[settings_output])

        with gr.Tab("Monitoring"):
            with gr.Group():
                gr.Markdown("## Current Settings")
                view_btn = gr.Button("View Settings")
                settings_view = gr.Textbox(label="Current Settings")
                view_btn.click(view_settings, outputs=[settings_view])
            
            with gr.Group():
                gr.Markdown("## User Statistics")
                users_btn = gr.Button("View Users")
                users_view = gr.Textbox(label="User Information")
                users_btn.click(view_users, outputs=[users_view])

        with gr.Tab("Database Management"):
            with gr.Group():
                gr.Markdown("## Clear Database")
                gr.Markdown("⚠️ Warning: These actions cannot be undone!")
                
                with gr.Row():
                    clear_users_btn = gr.Button("Clear User Data", variant="secondary")
                    clear_settings_btn = gr.Button("Clear Settings", variant="secondary")
                    clear_all_btn = gr.Button("Clear All Data", variant="stop")
                
                clear_status = gr.Textbox(label="Clear Status")
                
                clear_users_btn.click(clear_user_data, outputs=[clear_status])
                clear_settings_btn.click(clear_settings, outputs=[clear_status])
                clear_all_btn.click(clear_all_data, outputs=[clear_status])
                
        initialize_db()  # Set up database on startup
        
    return interface

# Create and launch the interface
interface = create_interface()

# Mount the Flask app within Gradio
app = gr.mount_gradio_app(app, interface, path="/")

if __name__ == "__main__":
    interface.launch(server_name="0.0.0.0", server_port=7860)
