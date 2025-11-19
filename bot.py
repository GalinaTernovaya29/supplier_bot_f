import os
import json
from flask import Flask, request
import telebot
from telebot.types import InputMediaPhoto

TOKEN = "8240072124:AAHz8TZSCltrxkLx4eyzCh84WgriGK3PfIo"  # вставь сюда токен
WEBHOOK_URL = "https://supplier-bot-f-3.onrender.com/"  # твой Render URL

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

DB_FILE = "database.json"
PHOTO_DIR = "photos"
os.makedirs(PHOTO_DIR, exist_ok=True)

if os.path.exists(DB_FILE):
    with open(DB_FILE, "r", encoding="utf-8") as f:
        suppliers = json.load(f)
else:
    suppliers = {}

# ---------- Helper functions ----------
def save_database():
    with open(DB_FILE, "w", encoding="utf-8") as f:
        json.dump(suppliers, f, ensure_ascii=False, indent=2)

def funny_response():
    responses = [
        "Ха-ха, я вас понял! 😎",
        "Ого! Интересный запрос, но попробуй фото или текст по инструкции 🐾",
        "Ну ты даёшь! Шутки и вопросы принимаю, но нужен запрос четко 😏"
    ]
    import random
    return random.choice(responses)

def find_photo_by_name(name_query):
    results = []
    for name, data in suppliers.items():
        if name_query.lower() in name.lower():
            results.append((name, data["photo"]))
    return results

# ---------- Handlers ----------
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Привет! Я бот поставщиков 😎\n"
        "📸 Загрузи фото поставщика с подписью или напиши его имя для поиска.\n"
        "Для добавления нового поставщика нужен **и текст, и фото**."
    )

@bot.message_handler(content_types=['text', 'photo'])
def handle_message(message):
    text = message.text.strip() if message.text else None
    photo = message.photo[-1] if message.photo else None

    # ----- Только текст -----
    if text and not photo:
        results = find_photo_by_name(text)
        if results:
            for name, photo_file in results:
                with open(photo_file, "rb") as f:
                    bot.send_photo(message.chat.id, f, caption=f"Поставщик: {name}")
        else:
            bot.send_message(message.chat.id, funny_response())
        return

    # ----- Фото с подписью -----
    if photo and text:
        file_info = bot.get_file(photo.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
        file_name = os.path.join(PHOTO_DIR, f"{file_info.file_id}.jpg")
        with open(file_name, "wb") as f:
            f.write(downloaded_file)

        if text in suppliers:
            bot.send_message(message.chat.id, f"Поставщик '{text}' уже есть в базе.")
        else:
            suppliers[text] = {"photo": file_name}
            save_database()
            bot.send_message(message.chat.id, f"Поставщик '{text}' добавлен ✅")
        return

    # ----- Фото без подписи или текст без фото -----
    if (photo and not text) or (text and not photo):
        bot.send_message(message.chat.id,
                         "Нужен и текст, и фото одновременно для добавления нового поставщика 🐾")
        return

    # ----- Любой другой текст -----
    bot.send_message(message.chat.id, funny_response())

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