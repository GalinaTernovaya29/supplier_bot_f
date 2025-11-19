import telebot
from telebot import types
import random
import os
import json

TOKEN = '8240072124:AAHz8TZSCltrxkLx4eyzCh84WgriGK3PfIo'
bot = telebot.TeleBot(TOKEN)

# Путь к базе
DB_PATH = 'database.json'

# Загрузка базы поставщиков
if os.path.exists(DB_PATH):
    with open(DB_PATH, 'r', encoding='utf-8') as f:
        db = json.load(f)
else:
    db = {}

# Приветствия, чередуются 1 к 5
greetings = [
    "Здравствуйте!",
    "Привет!",
    "Доброго дня!",
    "Рад вас видеть!",
    "Приветствую!"
]

# Юмор, строгий, 1 к 40
jokes = [
    "Мудрость приходит к тем, кто умеет ждать... хотя иногда спешка тоже помогает 😏",
    "Не спорь с дураком — люди могут не заметить разницы 🧐",
    "Лучше молчать и казаться глупцом, чем говорить и убедить всех в обратном 🤫",
    # ... до 40 штук
]

# Мудрые мысли, 1 к 30
wise_quotes = [
    "Тот, кто умеет слушать, слышит даже молчание 🌿",
    "Делай добро и бросай его в воду, оно вернется к тебе 🕊️",
    "Настоящая сила в умении сохранять спокойствие в бурю 🌊",
    # ... до 30 штук
]

# Временное хранилище фото перед подписанием
pending_photos = {}

# Функция случайного приветствия
def get_greeting():
    return random.choice(greetings)

# Функция случайного юмора
def get_joke():
    return random.choice(jokes)

# Функция мудрой мысли
def get_wise():
    return random.choice(wise_quotes)

# Старт / очистка чата
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_btn = types.KeyboardButton('Старт')
    markup.add(start_btn)
    bot.send_message(message.chat.id, f"{get_greeting()} Я ваш ИИ-консультант 🤖\n{get_wise()}", reply_markup=markup)

# Обработка текстовых сообщений
@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    text = message.text.strip()
    
    # Если ждем название после фото
    if chat_id in pending_photos:
        photo_file_id = pending_photos.pop(chat_id)
        db[text] = photo_file_id
        with open(DB_PATH, 'w', encoding='utf-8') as f:
            json.dump(db, f, ensure_ascii=False, indent=2)
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        markup.add(types.KeyboardButton('Старт'))
        bot.send_message(chat_id, "Сохранено ✅", reply_markup=markup)
        return

    # Поиск по тексту в базе
    if text in db:
        bot.send_photo(chat_id, db[text], caption=f"Найдено: {text}")
    else:
        bot.send_message(chat_id, f"Ого! Я такого поставщика не знаю 😏\nПопробуй загрузить фото, чтобы добавить его.")

# Обработка фото
@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    file_id = message.photo[-1].file_id

    # Проверка совпадений по фото
    found = False
    for name, pid in db.items():
        if pid == file_id:
            bot.send_message(chat_id, f"Уже есть: {name}")
            found = True
            break

    if not found:
        pending_photos[chat_id] = file_id
        bot.send_message(chat_id, "Фото принято! 🖼️ Пожалуйста, отправьте название поставщика:")

# ИИ-консультант (для любого текста без фото)
@bot.message_handler(func=lambda m: True)
def chat_ai(message):
    chat_id = message.chat.id
    if chat_id not in pending_photos:
        bot.send_message(chat_id, f"{get_joke()}")

bot.infinity_polling()