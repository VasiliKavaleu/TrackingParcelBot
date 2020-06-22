# -*- coding: utf-8 -*-

import telebot 
import re
import reference as rf
import keyboard as kb
from emoji import *
from load_page import *
from selenium import webdriver
from telebot import types
from flask import Flask, request

try:
    import config
    bot = telebot.TeleBot(config.token)
except Exception:
    token = os.environ.get("TOKEN")
    bot = telebot.TeleBot(token)
    local_host = False
else:
    local_host = True

sources = {00:'https://posylka.net/parcel/', 11:'https://1track.ru/tracking/'}
default_source = 00
item_does_not_tracking = 0

@bot.message_handler(regexp="Выбрать источник")
def handle_message(message):
    choose_source = 'Выберите, пожалуйста, источник поиска:' + '\n' + f'(по умолчанию {sources[default_source]})'
    bot.send_message(message.from_user.id, choose_source, reply_markup=kb.source_btn)

@bot.message_handler(regexp="Полезная информация")
def handle_message(message):
    faqanswer = 'Полезная информация' + envelope + mailbox
    bot.send_message(message.from_user.id, faqanswer, reply_markup=kb.faq)

@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    subbmit_msg = 'Изменения приняты ' + check + ' Спасибо за доверие' + sparkles
    if call.data == "0":
        bot.send_message(call.message.chat.id, rf.answ0)
    elif call.data == "1":
        bot.send_message(call.message.chat.id, rf.answ1)
    elif call.data == "2":
        bot.send_message(call.message.chat.id, rf.answ2)
    elif call.data == "3":
        bot.send_message(call.message.chat.id, rf.answ3)
    elif call.data == "4":
        bot.send_message(call.message.chat.id, rf.answ4)
    elif call.data == "00":
        default_source = 00
        bot.send_message(call.message.chat.id, subbmit_msg)
    elif call.data == "11":
        default_source = 11
        bot.send_message(call.message.chat.id, subbmit_msg)
    else:
        pass

@bot.message_handler(content_types=['text'])
def answer(message):
    t = '[A-Z]{2}[0-9]{9}[A-Z]{2}'
    if len(message.text) == 13 and re.match(t, message.text.upper()):  
        parsel_from_ali = GetInfo(message.text)
        proccesing_msg = 'Идет сбор информации..' + page + glass + globe
        bot.send_message(message.from_user.id, proccesing_msg)
        main_result_for_user = parsel_from_ali.run()
        if item_does_not_tracking == 0:
            bot.send_message(message.from_user.id, main_result_for_user)
        else:
            bot.send_message(message.from_user.id, main_result_for_user, reply_markup=kb.result_returnd_without_info)
    else:
        fault_masssage = 'Трек-номер не верного формата' + exclamation_emoji + 'Попробуйте еще раз ' + mobile_emoji
        bot.send_message(message.from_user.id, fault_masssage, reply_markup=kb.wrong_answer)

class GetInfo(Load, Parser):
    global item_does_not_tracking
    result = ''
    def __init__(self, item_num):
        self.item_num = item_num

    def run(self):
        if local_host:
            url = sources[default_source] + self.item_num
            html_page = Load.on_local(self, url)
            if default_source == 00:
                result = Parser.posylka(self, html_page)
            elif default_source == 11:
                result = Parser.track_ru(self, html_page)
            else:
                pass
        else :
            url = sources[default_source] + self.item_num
            html_page = Load.on_host(self, url)
            if default_source == 00:
                result = Parser.posylka(self, html_page)
            elif default_source == 11:
                result = Parser.track_ru(self, html_page)
            else:
                pass
        return f'Результат по запросу - {self.item_num} ' + arrow + '\n' + result 


if local_host == False:
    server = Flask(__name__)
    @server.route('/' + token, methods=['POST'])
    def getMessage():
        bot.process_new_updates([telebot.types.Update.de_json(request.stream.read().decode("utf-8"))])
        return "!", 200

    @server.route("/")
    def webhook():
        bot.remove_webhook()
        bot.set_webhook(url='https://bot-parsel.herokuapp.com/' + token)
        return "!", 200
    if __name__ == "__main__":
        server.run(host="0.0.0.0", port=int(os.environ.get('PORT', 5000)))
else:
    bot.remove_webhook()
    bot.polling(none_stop=True)


