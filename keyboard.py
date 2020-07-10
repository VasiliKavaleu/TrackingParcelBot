from telebot import types
from emoji import *


bottom_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
button_src = types.KeyboardButton('Выбрать источник отслеживания' + glass)
button_faq = types.KeyboardButton('Полезная информация' + eyes)
bottom_kb.add(button_src)
bottom_kb.add(button_faq)

quest0 = 'Простые и регистрируемые отправления.'
quest1 = 'Что такое трек-код (номер)?'
quest2 = 'Структура трек номера.'
quest3 = 'Как узнать номер отправления?'
quest4 = 'Не получается отследить посылку?'

btn0 = types.InlineKeyboardButton(text=quest0, callback_data='0')
btn1 = types.InlineKeyboardButton(text=quest1, callback_data='1')
btn2 = types.InlineKeyboardButton(text=quest2, callback_data='2')
btn3 = types.InlineKeyboardButton(text=quest3, callback_data='3')
btn4 = types.InlineKeyboardButton(text=quest4, callback_data='4')

faq = types.InlineKeyboardMarkup()
faq.add(btn0)
faq.add(btn1)
faq.add(btn2)
faq.add(btn3)
faq.add(btn4)

src1 = types.InlineKeyboardButton(text='posylka.net', callback_data='00')
src2 = types.InlineKeyboardButton(text='1track.ru', callback_data='11')

source_btn = types.InlineKeyboardMarkup()
source_btn.add(src1)
source_btn.add(src2)

wrong_answer = types.InlineKeyboardMarkup()
wrong_answer.add(btn1)
wrong_answer.add(btn2)
wrong_answer.add(btn3)

result_returnd_without_info = types.InlineKeyboardMarkup()
result_returnd_without_info.add(btn4)