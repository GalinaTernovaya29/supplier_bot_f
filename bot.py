# -*- coding: utf-8 -*-
bot.send_message(user_id, f"Добавлено: {supplier}")
return


# 2 — поиск по фото
db = load_db()
for supplier, items in db.items():
for item in items:
if item["file_id"] == file_id:
bot.send_message(user_id, generate_greeting())
bot.send_message(user_id, f"Совпадение найдено: {supplier}")
return


# 3 — если новое фото → просим текст
waiting_for_photo[user_id] = ""
bot.send_message(user_id, "Фото получено. Теперь напишите название поставщика ✍️")


# ----------------------------- СОХРАНЕНИЕ В БАЗУ -----------------------------
def save_new_pair(supplier, file_id):
db = load_db()
if supplier not in db:
db[supplier] = []
db[supplier].append({"supplier": supplier, "file_id": file_id})
save_db(db)


# ----------------------------- WEBHOOK -----------------------------
@server.route("/" + 8240072124:AAHz8TZSCltrxkLx4eyzCh84WgriGK3PfIo, methods=["POST"])
def process_update():
json_str = request.get_data().decode("utf-8")
update = telebot.types.Update.de_json(json_str)
bot.process_new_updates([update])
return "", 200


@server.route("/")
def webhook_info():
return "Бот работает.", 200


if __name__ == "__main__":
bot.remove_webhook()
bot.set_webhook(url=os.getenv("RENDER_EXTERNAL_URL", "") + "/" + TOKEN)
server.run(host="0.0.0.0", port=10000)