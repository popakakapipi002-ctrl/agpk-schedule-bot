from datetime import datetime, timedelta
import os
import requests
from bs4 import BeautifulSoup
import telebot
from flask import Flask, request

BOT_TOKEN = "8686197936:AAGPQ3_aDzzWiplC48bbKXuwYl8OO-fPeo0"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "Привет! Я бот с расписанием АГПК.")

@bot.message_handler(commands=['day'])
def day(message):
    today = datetime.now().strftime("%d.%m.%Y")
    monday = datetime.now() - timedelta(days=datetime.now().weekday())
    monday_str = monday.strftime("%d.%m.%Y")
    https://vk.ru/away.php?to=https%3A%2F%2Fwww.aspc-edu.ru%2Finformation%2Fedu%2Fschedule%2F%3Fgroup%3D115748%26date_edu1c%3D%7Btoday%7D%26send%3D%25D0%259F%25D0%25BE%25D0%25BA%25D0%25B0%25D0%25B7%25D0%25B0%25D1%2582%25D1%258C&utf=1

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Ищем все заголовки с датами (например, "24 СЕНТЯБРЯ 2026, ЧЕТВЕРГ")
    # Они обычно в <div> или <p> с текстом
    all_text = soup.get_text(separator='\n')
    lines = all_text.split('\n')

    target_date = datetime.now().strftime("%d.%m.%Y")
    result = f"Расписание на {target_date}:\n\n"
    found = False
    in_target_day = False

    for line in lines:
        line = line.strip()
        # Проверяем, начинается ли строка с даты
        if target_date in line and ('ПОНЕДЕЛЬНИК' in line or 'ВТОРНИК' in line or 'СРЕДА' in line or 'ЧЕТВЕРГ' in line or 'ПЯТНИЦА' in line or 'СУББОТА' in line):
            in_target_day = True
            continue
        # Если начался новый день — останавливаемся
        if in_target_day and ('ПОНЕДЕЛЬНИК' in line or 'ВТОРНИК' in line or 'СРЕДА' in line or 'ЧЕТВЕРГ' in line or 'ПЯТНИЦА' in line or 'СУББОТА' in line):
            break
        # Собираем строки с парами
        if in_target_day and line:
            result += line + '\n'
            found = True

    if not found:
        result += "На сегодня пар нет."

    bot.send_message(message.chat.id, result)
@bot.message_handler(commands=['week'])
def week(message):
    # Берём понедельник текущей недели
    monday = datetime.now() - timedelta(days=datetime.now().weekday())
    monday_str = monday.strftime("%d.%m.%Y")
   https://vk.ru/away.php?to=https%3A%2F%2Fwww.aspc-edu.ru%2Finformation%2Fedu%2Fschedule%2F%3Fgroup%3D115748%26date_edu1c%3D%7Btoday%7D%26send%3D%25D0%259F%25D0%25BE%25D0%25BA%25D0%25B0%25D0%25B7%25D0%25B0%25D1%2582%25D1%258C&utf=1

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    tables = soup.find_all('table')
    table = None
    for t in tables:
        if 'Дисциплина' in t.text:
            table = t
            break

    if not table:
        bot.send_message(message.chat.id, "Расписание не найдено.")
        return

    # Берём весь текст страницы, чтобы найти даты
    all_text = soup.get_text(separator='\n')
    lines = all_text.split('\n')

    result = "Расписание на неделю:\n\n"
    current_day = ""
    found = False

    for line in lines:
        line = line.strip()
        # Если строка — это дата (например, "24 СЕНТЯБРЯ 2026, ЧЕТВЕРГ")
        if any(day in line for day in ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА']) and '2026' in line:
            current_day = line
            result += f"\n{current_day}\n"
            found = True
        # Если строка — это пара (начинается с цифры)
        elif found and line and line[0].isdigit():
            result += line + '\n'

    if not found:
        result = "Расписание не найдено."

    bot.send_message(message.chat.id, result)
@app.route('/' + BOT_TOKEN, methods=['POST'])
def getMessage():
    json_string = request.get_data().decode('utf-8')
    update = telebot.types.Update.de_json(json_string)
    bot.process_new_updates([update])
    return "!", 200

@app.route('/health')
def health():
    return "OK", 200

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url="https://agpk-schedule-bot.onrender.com/" + BOT_TOKEN)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)


