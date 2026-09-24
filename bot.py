import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
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
    url = f"https://www.aspc-edu.ru/information/edu/schedule/?group=115748&date_edu1c={today}&send=Показать"

    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table')

    if not table:
        bot.send_message(message.chat.id, "Расписание не найдено.")
        return

    result = f"Расписание на {today}:\n\n"
    rows = table.find_all('tr')

    for row in rows:
        cells = row.find_all('td')
        if len(cells) >= 4:
            para = cells[0].text.strip()
            subject = cells[2].text.strip()
            room = cells[3].text.strip()
            result += f"{para} пара | {subject} | {room}\n"

    bot.send_message(message.chat.id, result)

@bot.message_handler(commands=['week'])
def week(message):
    bot.send_message(message.chat.id, "Расписание на неделю (пока пусто)")

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






