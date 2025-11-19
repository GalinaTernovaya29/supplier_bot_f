import telebot
from telebot import types
import json
import random
import os

TOKEN = "<8240072124:AAHz8TZSCltrxkLx4eyzCh84WgriGK3PfIo>"
bot = telebot.TeleBot(TOKEN)

DB_FILE = 'database.json'

# Загрузка базы
if os.path.exists(DB_FILE):
    with open(DB_FILE, 'r', encoding='utf-8') as f:
        database = json.load(f)
else:
    database = {}

# Приветствия, шутки и мудрые мысли
greetings = [
    "Здравствуйте!",
    "Привет!",
    "Добрый день!",
    "Рад видеть вас!",
    "С добром!"
]

jokes = [
    "Жизнь — это то, что с тобой происходит, пока ты строишь планы. 😏",
    "Не откладывай на завтра то, что можно оставить на послезавтра.",
    "Утро вечера мудренее… особенно если утром кофе.",
    "Чем старше становишься, тем меньше хочется делиться секретами с миром.",
    "Не спорь с дураком — люди могут не заметить разницы.",
    "Иногда тишина — лучший ответ на глупость.",
    "Если бы лень была видом спорта, я был бы чемпионом.",
    "Век живи — век учись, а на работу ходи.",
    "Каждое утро — шанс напомнить миру, что ты проснулся.",
    "Счастье — это когда кофе горячий, а Wi-Fi быстрый."
]  # Добавь до 40 штук

wisdom = [
    "Не тот велик, кто никогда не падал, а тот велик, кто падал и вставал.",
    "Кто ищет — тот всегда найдет.",
    "Слово не воробей: вылетит — не поймаешь, а мудрое останется навсегда.",
    "Терпение и труд всё перетрут.",
    "Истинная сила — в умении прощать.",
    "Лучше сделать и пожалеть, чем не сделать и жалеть.",
    "Смелость — не отсутствие страха, а умение действовать несмотря на него.",
    "Доброта — это язык, который слышит каждый.",
    "Мудрость приходит с опытом, а не с годами.",
    "Знание без действия — это просто информация."
]  # Добавь до 30 штук

# Хранилище ожидающих названий
awaiting_name = {}

# Основной обработчик
@bot.message_handler(content_types=['text', 'photo'])
def handle_message(message):
    chat_id = message.chat.id

    # Если фото
    if message.content_type == 'photo':
        file_id = message.photo[-1].file_id
        file_info = bot.get_file(file_id)
        file_path = file_info.file_path
        file_name = f"{file_id}.jpg"

        # Скачиваем
        downloaded_file = bot.download_file(file_path)
        with open(f'photos/{file_name}', 'wb') as f:
            f.write(downloaded_file)

        # Проверяем совпадение
        if file_name in database:
            bot.send_message(chat_id, f"Совпадение найдено:\nФото: {file_name}\nПоставщик: {database[file_name]}")
        else:
            awaiting_name[chat_id] = file_name
            bot.send_message(chat_id, "Фото получено, но нужно название поставщика для сохранения. Пожалуйста, отправьте название.")

    # Если текст
    elif message.content_type == 'text':
        # Если ждем название для фото
        if chat_id in awaiting_name:
            file_name = awaiting_name.pop(chat_id)
            database[file_name] = message.text
            with open(DB_FILE, 'w', encoding='utf-8') as f:
                json.dump(database, f, ensure_ascii=False, indent=4)
            bot.send_message(chat_id, f"Сохранено: {file_name} → {message.text}")
        else:
            # Поиск по тексту
            matches = [k for k, v in database.items() if v.lower() == message.text.lower()]
            if matches:
                msg = "Найдены совпадения:\n" + "\n".join([f"{k} → {database[k]}" for k in matches])
                bot.send_message(chat_id, msg)
            else:
                bot.send_message(chat_id, "Совпадений нет. Если хотите добавить новый, пришлите фото и подпишите его названием.")

# ИИ-консультант
@bot.message_handler(func=lambda m: True)
def ai_response(message):
    chat_id = message.chat.id
    text = message.text

    # 1 из 10 шуток
    if random.randint(1, 10) == 1:
        bot.send_message(chat_id, random.choice(jokes))
    # 1 из 30 мудрых мыслей
    elif random.randint(1, 30) == 1:
        bot.send_message(chat_id, random.choice(wisdom))
    else:
        bot.send_message(chat_id, "Я вас слышу 😏")

# Запуск
if __name__ == "__main__":
    if not os.path.exists('photos'):
        os.mkdir('photos')
    bot.polling(none_stop=True)