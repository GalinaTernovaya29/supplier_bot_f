import telebot
import random
import os
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

# ================== Настройка ==================
TOKEN = '8240072124:AAHz8TZSCltrxkLx4eyzCh84WgriGK3PfIo'
bot = telebot.TeleBot(TOKEN)

# ================== Данные ==================
# Приветствия 1 к 5
greetings = [
    "Здравствуйте!",
    "Привет!",
    "Добрый день!",
    "Рада видеть вас!",
    "Приветствую!"
]

# Шутки 1 к 40 (строгие, изысканные)
jokes = [
    "Не торопись, умный видит дальше.",
    "Кто ищет лёгкие пути, тот сам себе тяжёлый груз.",
    "Иногда молчание говорит больше, чем слова.",
    "Человек смеётся не от счастья, а от здравого смысла.",
    "Смех — это искра, а мудрость — огонь.",
    "Кто видит без ошибок, тот видит глубже.",
    "Юмор — зеркало ума, а не глупости.",
    "Смешно тому, кто видит правду сквозь хаос.",
    "Шутка, сказанная вовремя, ценнее тысячи слов.",
    "Тот, кто смеётся над собой, управляет миром эмоций.",
    # ...добавь до 40 по аналогии
]

# Мудрые мысли 1 к 30
wisdoms = [
    "Сила человека — в его уме и сердце, а не в кулаках.",
    "Тот, кто знает пределы, управляет собой.",
    "Поступай так, чтобы завтра не стыдно было за сегодня.",
    "Истинная свобода приходит с ответственностью.",
    "Терпение — это ключ к мастерству.",
    "Каждое действие оставляет след, выбирай осознанно.",
    "Слова могут исцелять или ранить — выбирай мудро.",
    "Знание без действия — пустой дар.",
    "Прощение освобождает душу больше, чем обида.",
    "Тишина иногда громче сотни слов.",
    # ...добавь до 30 по аналогии
]

# База поставщиков (для примера, в будущем - sqlite или json)
supplier_db = {}  # {название: фото_file_id}

# ================== Кнопки ==================
def start_keyboard():
    markup = ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add(KeyboardButton('/start'))
    return markup

# ================== Состояния пользователей ==================
user_states = {}  # chat_id: {'waiting_for_name': False, 'last_photo_id': None}

# ================== Обработчики ==================
@bot.message_handler(commands=['start'])
def handle_start(message):
    chat_id = message.chat.id
    user_states[chat_id] = {'waiting_for_name': False, 'last_photo_id': None}
    greet = random.choice(greetings)
    bot.send_message(chat_id, f"{greet} Я готова к работе! 📸 Направьте фото или текст.", reply_markup=start_keyboard())

@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    chat_id = message.chat.id
    photo_id = message.photo[-1].file_id
    text = message.caption.strip() if message.caption else ''
    
    if text:  # фото + текст
        supplier_db[text.lower()] = photo_id
        user_states[chat_id] = {'waiting_for_name': False, 'last_photo_id': None}
        bot.send_message(chat_id, f"Фото с названием '{text}' сохранено ✅")
    else:  # только фото
        user_states[chat_id] = {'waiting_for_name': True, 'last_photo_id': photo_id}
        bot.send_message(chat_id, "Нужен текст с названием поставщика для сохранения фото. Пожалуйста, пришлите название.")

@bot.message_handler(content_types=['text'])
def handle_text(message):
    chat_id = message.chat.id
    text = message.text.strip().lower()
    
    if text == '/start':
        handle_start(message)
        return
    
    state = user_states.get(chat_id, {'waiting_for_name': False, 'last_photo_id': None})
    
    if state['waiting_for_name'] and state['last_photo_id']:
        supplier_db[text] = state['last_photo_id']
        user_states[chat_id] = {'waiting_for_name': False, 'last_photo_id': None}
        bot.send_message(chat_id, f"Фото с названием '{text}' сохранено ✅")
        return
    
    # Проверка текста в базе
    if text in supplier_db:
        photo_id = supplier_db[text]
        bot.send_photo(chat_id, photo_id, caption=f"Найдено совпадение: {text}")
    else:
        # Шутка/мудрость случайная
        reply_type = random.randint(1, 10)
        if reply_type == 1:
            joke = random.choice(jokes)
            bot.send_message(chat_id, f"😏 {joke}")
        elif reply_type <= 4:
            wisdom = random.choice(wisdoms)
            bot.send_message(chat_id, f"💡 {wisdom}")
        else:
            bot.send_message(chat_id, "Ого! Попробуй фото или текст по инструкции 🐾")

# ================== Запуск ==================
bot.infinity_polling()