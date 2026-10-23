import os
from http.server import HTTPServer, BaseHTTPRequestHandler
import threading
import telebot

# Render ke liye dummy web server (Port error hatane ke liye)
class SimpleHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()
        self.wfile.write(b"HRIX Store Bot is Live!")

def run_server():
    port = int(os.environ.get("PORT", 10000))
    server = HTTPServer(("0.0.0.0", port), SimpleHandler)
    server.serve_forever()

# Server ko background thread mein chalayein
server_thread = threading.Thread(target=run_server)
server_thread.daemon = True
server_thread.start()

# Aapka Sahi Telegram Bot Token
TOKEN = '8809123081:AAFsGG-i-qzzof-buot91gJTMZ86LlbxFGM'
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.reply_to(message, "Welcome to HRIX Store! Aapka bot safalpurvak chalu ho gaya hai.")

# Bot ko chalu rakhne ke liye
bot.infinity_polling()
