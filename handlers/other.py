from aiogram import types, Dispatcher
import json
import string
from create_bot import dp

#@dp.message_handler()
async def echo_sendler(message : types.Message):
    if {i.lower().translate(str.maketrans('', '', string.punctuation)) for i in message.text.split(' ')}\
        .intersection(set(json.load(open('spisok.json')))) != set():
        await message.reply('Материться нельзя')
        await message.delete()

def registor_handlers_other(dp : Dispatcher):
    dp.register_message_handler(echo_sendler)
