from aiogram import types, Dispatcher
from create_bot import dp, bot
from keyboards import kb_client
from aiogram.types import ReplyKeyboardRemove
from data_base import sqlite_db

#@dp.message_handler(commands=['start', 'help'])
async def command_start(message : types.Message):
    sqlite_db.sql_start()
    try:
        await bot.send_message(message.from_user.id, 'Здравствуйте. Подключение прошло успешно', reply_markup=kb_client)
        await message.delete()
    except:
        await message.reply('Общение с ботом происходит в ЛС, напиши ему: \https://t.me/my_portfolio_2_bot')

# #@dp.message_handler(commands=['подключить'])
# async def pod(message: types.Message):
#
#     await bot.send_message(message.from_user.id, 'Готово епта')

#@dp.message_handler(commands=['Режим_работы'])
async def command_open_restoran(message : types.Message):
    try:
        await message.answer('Режим работы: 24/7')
        #await message.delete()
    except:
        await message.reply('Общение с ботом происходит в ЛС, напиши ему: \https://t.me/my_portfolio_2_bot')

#@dp.message_handler(commands=['Где_вы_находитесь'])
async def command_where(message : types.Message):
    try:
        await message.answer('Красная дом 999')# ,reply_markup=ReplyKeyboardRemove())
        #await message.delete()
    except:
        await message.reply('Общение с ботом происходит в ЛС, напиши ему: \https://t.me/my_portfolio_2_bot')
# @dp.message_handler(commands=['Меню'])
async def pizza_menu_command(message : types.Message):
    await sqlite_db.sql_read(message)

def registor_handlers_client(dp : Dispatcher):
    dp.register_message_handler(command_start, commands=['start', 'help'])
    dp.register_message_handler(command_open_restoran, commands=['Режим_работы'])
    dp.register_message_handler(command_where, commands=['Где_вы_находитесь'])
    dp.register_message_handler(pizza_menu_command, commands=['Меню'])
    # dp.register_message_handler(pod, commands=['подключить'])
