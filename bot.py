import os
from flask import Flask, request
import telebot  # pip install pyTelegramBotAPI

TOKEN = "8240072124:AAHz8TZSCltrxkLx4eyzCh84WgriGK3PfIo"  # <-- вставь сюда токен
WEBHOOK_URL = "https://supplier-bot-f-2.onrender.com/"  # <-- твой Render URL

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# ---------- Telegram handlers ----------
@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, "Привет! Бот работает 24/7 на Render 🚀")

@bot.message_handler(func=lambda message: True)
def echo_all(message):
    bot.send_message(message.chat.id, f"Вы написали: {message.text}")

# ---------- Webhook route ----------
@app.route("/", methods=["POST"])
def webhook():
    json_str = request.get_data().decode("utf-8")
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

# ---------- Set webhook ----------
bot.remove_webhook()
bot.set_webhook(url=WEBHOOK_URL)

# ---------- Run Flask ----------
if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=PORT)