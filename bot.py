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
    url = f"https://www.aspc-edu.ru/information/edu/schedule/?group=115748&date_edu1c={today}"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    all_text = soup.get_text(separator='\n')
    lines = all_text.split('\n')
    
    result = f"Расписание на {today}:\n\n"
    found = False
    in_target_day = False
    
    for line in lines:
        line = line.strip()
        if today in line and any(day in line for day in ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА']):
            in_target_day = True
            continue
        if in_target_day and any(day in line for day in ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА']):
            break
        if in_target_day and line:
            result += line + '\n'
            found = True
    
    if not found:
        result += "На сегодня пар нет."
    
    bot.send_message(message.chat.id, result)
@bot.message_handler(commands=['week'])
def week(message):
    monday = datetime.now() - timedelta(days=datetime.now().weekday())
    monday_str = monday.strftime("%d.%m.%Y")
    url = f"https://www.aspc-edu.ru/information/edu/schedule/?group=115748&date_edu1c={monday_str}"
    
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    
    all_text = soup.get_text(separator='\n')
    lines = all_text.split('\n')
    
    result = "Расписание на неделю:\n\n"
    found = False
    
    for line in lines:
        line = line.strip()
        if any(day in line for day in ['ПОНЕДЕЛЬНИК', 'ВТОРНИК', 'СРЕДА', 'ЧЕТВЕРГ', 'ПЯТНИЦА', 'СУББОТА']) and '2026' in line:
            result += f"\n{line}\n"
            found = True
        elif found and line and (line[0].isdigit() or line.startswith('МДК')):
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


