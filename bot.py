<<<<<<< HEAD
import os
import sqlite3
from PIL import Image
from io import BytesIO
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random

# Токен из переменной окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("Не найден токен! Убедись, что переменная среды TELEGRAM_TOKEN установлена.")

# Подключаем SQLite
conn = sqlite3.connect("database.sqlite", check_same_thread=False)
cursor = conn.cursor()

# Создаём таблицу, если нет
cursor.execute('''
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    photo BLOB
)
''')
conn.commit()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Загрузи фото стикера или коробки, и я помогу определить поставщика. 😊"
    )

# Функция проверки фото на дубликат
def is_photo_duplicate(photo_bytes):
    cursor.execute("SELECT photo FROM suppliers")
    for (existing_photo,) in cursor.fetchall():
        if existing_photo == photo_bytes:
            return True
    return False

# Функция проверки имени поставщика
def is_name_duplicate(name):
    cursor.execute("SELECT name FROM suppliers WHERE name=?", (name,))
    return cursor.fetchone() is not None

# Юмористический ответ
def random_reply():
    replies = [
        "Ого, такой у нас ещё не было!",
        "Ха-ха, новый поставщик в базе!",
        "Всё по-научному, записываю!",
        "Такого фото у меня ещё не встречалось!",
        "Ну это уже шедевр, сохраняем!"
    ]
    return random.choice(replies)

# Обработка фото
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("Хм, это не похоже на фото...")
        return

    # Берём самое большое фото
    photo_file = await update.message.photo[-1].get_file()
    bio = BytesIO()
    await photo_file.download(out=bio)
    photo_bytes = bio.getvalue()

    # Проверяем дубликат
    if is_photo_duplicate(photo_bytes):
        await update.message.reply_text("Такое фото уже есть в базе. Попробуй добавить описание.")
        return

    # Сохраняем фото в контексте для следующего шага
    context.user_data["photo_bytes"] = photo_bytes
    await update.message.reply_text("Фото получено! А теперь напиши название поставщика, пожалуйста.")

# Обработка текста
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    photo_bytes = context.user_data.get("photo_bytes")

    if not photo_bytes:
        # Поиск по имени
        cursor.execute("SELECT photo FROM suppliers WHERE name=?", (name,))
        result = cursor.fetchone()
        if result:
            await update.message.reply_text(f"Нашёл поставщика '{name}' в базе! 😊")
        else:
            await update.message.reply_text("Поставщик не найден. Сначала загрузи фото.")
        return

    # Проверка на дубликат имени
    if is_name_duplicate(name):
        await update.message.reply_text("Такое имя уже есть для другой записи. Попробуй другое.")
        return

    # Сохраняем в базу
    cursor.execute("INSERT INTO suppliers (name, photo) VALUES (?, ?)", (name, photo_bytes))
    conn.commit()
    context.user_data.pop("photo_bytes", None)

    # Юмор
    await update.message.reply_text(random_reply())

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("Бот запущен...")
=======
import os
import sqlite3
from PIL import Image
from io import BytesIO
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
import random

# Токен из переменной окружения
TOKEN = os.getenv("TELEGRAM_TOKEN")
if not TOKEN:
    raise ValueError("Не найден токен! Убедись, что переменная среды TELEGRAM_TOKEN установлена.")

# Подключаем SQLite
conn = sqlite3.connect("database.sqlite", check_same_thread=False)
cursor = conn.cursor()

# Создаём таблицу, если нет
cursor.execute('''
CREATE TABLE IF NOT EXISTS suppliers (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    photo BLOB
)
''')
conn.commit()

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Привет! Загрузи фото стикера или коробки, и я помогу определить поставщика. 😊"
    )

# Функция проверки фото на дубликат
def is_photo_duplicate(photo_bytes):
    cursor.execute("SELECT photo FROM suppliers")
    for (existing_photo,) in cursor.fetchall():
        if existing_photo == photo_bytes:
            return True
    return False

# Функция проверки имени поставщика
def is_name_duplicate(name):
    cursor.execute("SELECT name FROM suppliers WHERE name=?", (name,))
    return cursor.fetchone() is not None

# Юмористический ответ
def random_reply():
    replies = [
        "Ого, такой у нас ещё не было!",
        "Ха-ха, новый поставщик в базе!",
        "Всё по-научному, записываю!",
        "Такого фото у меня ещё не встречалось!",
        "Ну это уже шедевр, сохраняем!"
    ]
    return random.choice(replies)

# Обработка фото
async def handle_photo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message.photo:
        await update.message.reply_text("Хм, это не похоже на фото...")
        return

    # Берём самое большое фото
    photo_file = await update.message.photo[-1].get_file()
    bio = BytesIO()
    await photo_file.download(out=bio)
    photo_bytes = bio.getvalue()

    # Проверяем дубликат
    if is_photo_duplicate(photo_bytes):
        await update.message.reply_text("Такое фото уже есть в базе. Попробуй добавить описание.")
        return

    # Сохраняем фото в контексте для следующего шага
    context.user_data["photo_bytes"] = photo_bytes
    await update.message.reply_text("Фото получено! А теперь напиши название поставщика, пожалуйста.")

# Обработка текста
async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    name = update.message.text.strip()
    photo_bytes = context.user_data.get("photo_bytes")

    if not photo_bytes:
        # Поиск по имени
        cursor.execute("SELECT photo FROM suppliers WHERE name=?", (name,))
        result = cursor.fetchone()
        if result:
            await update.message.reply_text(f"Нашёл поставщика '{name}' в базе! 😊")
        else:
            await update.message.reply_text("Поставщик не найден. Сначала загрузи фото.")
        return

    # Проверка на дубликат имени
    if is_name_duplicate(name):
        await update.message.reply_text("Такое имя уже есть для другой записи. Попробуй другое.")
        return

    # Сохраняем в базу
    cursor.execute("INSERT INTO suppliers (name, photo) VALUES (?, ?)", (name, photo_bytes))
    conn.commit()
    context.user_data.pop("photo_bytes", None)

    # Юмор
    await update.message.reply_text(random_reply())

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.PHOTO, handle_photo))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    print("Бот запущен...")
>>>>>>> 5b228fddc404baddbb96ed5605414fbb2613f6ab
    app.run_polling()