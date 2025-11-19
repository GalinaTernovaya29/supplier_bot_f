import os
import threading
from http.server import HTTPServer, BaseHTTPRequestHandler
import telebot  # pip install pyTelegramBotAPI

# Fake server для Render
PORT = int(os.environ.get("PORT", 5000))
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Bot is running!")
threading.Thread(target=lambda: HTTPServer(("0.0.0.0", PORT), Handler).serve_forever(), daemon=True).start()

# Telegram-бот
TOKEN = "8240072124:AAHz8TZSCltrxkLx4eyzCh84WgriGK3PfIo"  # <-- вставь сюда токен
bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Бот работает 24/7 на Render 🚀")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"Вы написали: {message.text}")

bot.infinity_polling()