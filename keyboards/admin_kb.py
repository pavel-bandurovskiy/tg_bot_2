from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove

"""Клаватура для админа"""
button_load = KeyboardButton('/Загрузить')
button_del = KeyboardButton('/Удалить')

button_case_admin = ReplyKeyboardMarkup(resize_keyboard = True).add(button_load).add(button_del)
