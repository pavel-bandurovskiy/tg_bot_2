from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

#b0 = KeyboardButton('/подключить')
b1 = KeyboardButton('/Режим_работы')
b2 = KeyboardButton('/Где_вы_находитесь')
b3 = KeyboardButton('/Меню')
b4 = KeyboardButton('Поделиться геопозицией', request_location=True)
b5 = KeyboardButton('Поделиться номером телефона', request_contact=True)

kb_client = ReplyKeyboardMarkup(resize_keyboard=True)#, one_time_keyboard=True)

kb_client.insert(b1).insert(b2).add(b3).row(b4,b5)
