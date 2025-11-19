import telebot
from telebot import types
import json
import random
import os

TOKEN = '8240072124:AAHz8TZSCltrxkLx4eyzCh84WgriGK3PfIo'  # твой токен
bot = telebot.TeleBot(TOKEN, parse_mode='HTML')

DATABASE_FILE = 'database.json'

# Создаем или загружаем базу
if not os.path.exists(DATABASE_FILE):
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump([], f, ensure_ascii=False, indent=4)

with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
    database = json.load(f)

# Приветствия 1 к 5
greetings = [
    "Здравствуйте!",
    "Привет!",
    "Добрый день!",
    "Рад видеть вас!",
    "Приветствую!"
]

# Юмор 1 к 40 (изысканный, строгий)
humor = [
    "Шутки в сторону, но иногда стоит улыбнуться. 😉",
    "В мире серых будней ирония — редкая роскошь.",
    "Смех — секретный соус к серьезным делам.",
    "Юмор — как специя: без меры плохо, с мерой вкусно.",
    "Даже шахматная партия требует лёгкой улыбки.",
    "Смеётся тот, кто понимает, что жизнь — это тест.",
    "Сарказм иногда дороже золота.",
    "Шутки — как кофе, бодрят мысли.",
    "Ирония делает строгие истины мягче.",
    "Смех — это уважение к нелепости мира.",
    # ... добавьте до 40
]

# Мудрые мысли 1 к 30
wisdoms = [
    "Сделанное с умом лучше, чем сделанное в спешке.",
    "Каждое действие оставляет след в памяти мира.",
    "Тот, кто ищет знания, никогда не заблудится.",
    "Слова без дела пусты, а дело без мысли опасно.",
    "Мудрость растет там, где терпение живет.",
    "Сила духа проявляется в тишине решений.",
    "Настоящее богатство — внутреннее спокойствие.",
    "Уважение к себе рождает уважение к другим.",
    "Лучше маленький шаг к цели, чем большой отступ.",
    "Истинное знание — осознанная практика.",
    # ... добавьте до 30
]

# Хранилище промежуточных фото для новых поставщиков
pending_photos = {}

# Кнопка старт
def start_keyboard():
    keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
    keyboard.add("Старт")
    return keyboard

# Очистка чата (только для новых фото/текста)
def clear_pending(user_id):
    if user_id in pending_photos:
        del pending_photos[user_id]

# Обработчик команды /start и кнопки "Старт"
@bot.message_handler(commands=['start'])
@bot.message_handler(func=lambda m: m.text == "Старт")
def handle_start(message):
    user_id = message.from_user.id
    clear_pending(user_id)
    greeting = random.choice(greetings)
    bot.send_message(message.chat.id, f"{greeting}\nБот готов. Загружайте фото или текст.", reply_markup=start_keyboard())

# Обработка фото
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    user_id = message.from_user.id
    photo_id = message.photo[-1].file_id

    # Ищем совпадение в базе
    found = None
    for item in database:
        if photo_id == item.get('photo_id'):
            found = item
            break

    if found:
        bot.send_message(message.chat.id, f"Найдено совпадение:\nНазвание: {found['name']}")
        bot.send_photo(message.chat.id, photo_id)
    else:
        pending_photos[user_id] = photo_id
        bot.send_message(message.chat.id, "Фото получено. Пожалуйста, пришлите название поставщика, иначе фото не сохранится.")

# Обработка текста
@bot.message_handler(func=lambda m: True)
def handle_text(message):
    user_id = message.from_user.id
    text = message.text.strip()

    if user_id in pending_photos:
        # Сохраняем новое фото с названием
        new_entry = {'name': text, 'photo_id': pending_photos[user_id]}
        database.append(new_entry)
        with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
            json.dump(database, f, ensure_ascii=False, indent=4)
        bot.send_message(message.chat.id, "Сохранено ✅", reply_markup=start_keyboard())
        clear_pending(user_id)
        return

    # Проверка по базе без фото
    found = [item for item in database if text.lower() in item['name'].lower()]
    if found:
        for item in found:
            bot.send_message(message.chat.id, f"Найдено совпадение: {item['name']}")
            bot.send_photo(message.chat.id, item['photo_id'])
    else:
        bot.send_message(message.chat.id, "Фото не найдено. Пожалуйста, пришлите фото для поиска.")

# ИИ-консультант (шутки + мудрости)
@bot.message_handler(func=lambda m: True)
def ai_consultant(message):
    humor_msg = random.choice(humor)
    wisdom_msg = random.choice(wisdoms)
    bot.send_message(message.chat.id, f"{humor_msg}\n{wisdom_msg}")

# Webhook (Render)
from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["POST"])
def webhook():
    json_str = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))