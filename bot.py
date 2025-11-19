import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton
import os
import json
import random
import time

TOKEN = '8240072124:AAHz8TZSCltrxkLx4eyzCh84WgriGK3PfIo'  # твой токен
bot = telebot.TeleBot(TOKEN)

# Файлы базы
DATABASE_FILE = 'database.json'

# Загрузка базы
if os.path.exists(DATABASE_FILE):
    with open(DATABASE_FILE, 'r', encoding='utf-8') as f:
        database = json.load(f)
else:
    database = []

# Приветствия 1 к 5
greetings = ["Здравствуйте!", "Привет!", "Добрый день!", "Рад видеть!", "Приветствую!"]

# Юмор 1 к 40 (изысканный, строгий)
humor_list = [
    "Иногда молчание громче слов, но не у всех хватает терпения это заметить.",
    "Даже часы, остановившись, дважды в день показывают точное время.",
    "Люди часто спорят о важном, забывая о главном.",
    "Лучше однажды посмеяться над собой, чем всю жизнь над другими.",
    "Тот, кто слишком серьёзно относится к шуткам, их не понимает.",
    "В каждой шутке есть крупица истины, но не всякая крупица достойна внимания.",
    "Смех — это мост между глупостью и мудростью.",
    "Некоторые шутки лучше хранить в тетради, а не в устах.",
    "Хитрость без смеха скучна, смех без хитрости — наивен.",
    "Сарказм — это тонкая кисть, а не молоток."
] * 4  # 40 вариантов

# Мудрые мысли 1 к 30
wise_list = [
    "Слово не воробей, вылетит — не поймаешь.",
    "Кто ищет, тот всегда найдёт, но не всегда то, что ожидал.",
    "Время — лучший учитель, но к сожалению, убивает всех своих учеников.",
    "Человек узнаёт себя в деле, а не в словах.",
    "Терпение и труд всё перетрут, кроме лени.",
    "Истинная мудрость в умении слушать.",
    "Не тот силён, кто побеждает других, а кто побеждает себя.",
    "Пусть твои поступки говорят громче слов.",
    "Кто рано встаёт, тому не всегда удаётся, зато он живёт дольше.",
    "Счастье любит тишину и сосредоточенность.",
    "Мир любит тех, кто умеет ждать и действовать.",
    "Люди забывают слова, но помнят дела.",
    "Не бойся ошибок — бойся их повторения.",
    "Лучше сделать и пожалеть, чем не сделать и мучиться.",
    "Красота в простоте, сила — в ясности мысли.",
    "Доброта возвращается тем, кто умеет её давать.",
    "Жизнь — это не количество вдохов, а моменты, от которых захватывает дух.",
    "Учись видеть невидимое, слышать неслышное, чувствовать неощутимое.",
    "Поступок человека измеряется не словами, а результатом.",
    "Чем выше цель, тем острее ответственность.",
    "Не ищи лёгких путей — ищи правильные.",
    "Мудрость приходит, когда исчезает гордыня.",
    "Истина часто скрыта в деталях.",
    "Лучше понять, чем быть понятым.",
    "Сила в том, чтобы вовремя остановиться.",
    "Каждое начало таит конец, и каждое завершение — новое начало.",
    "Величие в скромности.",
    "Не трать жизнь на ненужное.",
    "Люби мир таким, какой он есть, а не каким хотел бы.",
    "Слушай больше, говори меньше."
]

# Состояния пользователей: {user_id: {"photo": last_photo_id}}
user_state = {}

# Кнопка старт
def start_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton("Старт"))
    return markup

# Случайное приветствие + мудрость + юмор
def welcome_message():
    greet = random.choice(greetings)
    wise = random.choice(wise_list)
    humor = random.choice(humor_list)
    return f"{greet}\n\n💡 {wise}\n\n😏 {humor}"

# Обновление базы
def save_database():
    with open(DATABASE_FILE, 'w', encoding='utf-8') as f:
        json.dump(database, f, ensure_ascii=False, indent=2)

# Проверка по фото
def find_by_photo(photo_id):
    for item in database:
        if item.get("photo_id") == photo_id:
            return item
    return None

# Проверка по тексту
def find_by_text(text):
    for item in database:
        if item.get("name").lower() == text.lower():
            return item
    return None

# Обработчик /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    user_state[message.chat.id] = {}
    bot.send_message(message.chat.id, welcome_message(), reply_markup=start_keyboard())

# Обработчик всех сообщений
@bot.message_handler(content_types=['text', 'photo'])
def handle_message(message):
    user_id = message.chat.id

    # Начало
    if message.text == "Старт":
        user_state[user_id] = {}
        bot.send_message(user_id, welcome_message())
        return

    # Фото
    if message.content_type == 'photo':
        photo_id = message.photo[-1].file_id
        item = find_by_photo(photo_id)
        if item:
            bot.send_photo(user_id, photo_id, caption=f"Найдено в базе: {item['name']}")
        else:
            user_state[user_id] = {"photo": photo_id, "awaiting_name": True}
            bot.send_message(user_id, "📸 Фото получено. Пожалуйста, пришлите название поставщика.")
        return

    # Текст
    if message.content_type == 'text':
        text = message.text.strip()
        state = user_state.get(user_id, {})

        # Ожидание названия после фото
        if state.get("awaiting_name") and state.get("photo"):
            database.append({"photo_id": state["photo"], "name": text})
            save_database()
            bot.send_message(user_id, f"✅ Сохранено: {text}", reply_markup=start_keyboard())
            user_state[user_id] = {}
            return

        # Поиск по тексту
        item = find_by_text(text)
        if item:
            bot.send_photo(user_id, item["photo_id"], caption=f"Найдено по тексту: {item['name']}")
        else:
            bot.send_message(user_id, "❗ Не найдено. Пожалуйста, пришлите фото для добавления в базу.")
        return

# Запуск бота
# bot.infinity_polling()