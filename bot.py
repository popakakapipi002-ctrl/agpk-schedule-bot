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
    url = "https://www.aspc-edu.ru/information/edu/schedule/?group=115748"
    response = requests.get(url)
    text = response.text[:1000]
    bot.send_message(message.chat.id, f"Вот что видит бот:\n\n{text}")
@bot.message_handler(commands=['week'])
def week(message):
    url = "https://www.aspc-edu.ru/information/edu/schedule/?group=115748"
    response = requests.get(url)
    text = response.text[:1000]
    bot.send_message(message.chat.id, f"Вот что видит бот:\n\n{text}")
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


