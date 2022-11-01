from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Text
from create_bot import dp, bot
from data_base import sqlite_db
from keyboards import admin_kb
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

ID = None

class FSMAdmin(StatesGroup):
    photo = State()
    name = State()
    description = State()
    price = State()

"""Проверка на модератора группы"""
#@dp.message_handler(commands=['moderator'], is_chat_admin=True)
async def make_change_comand(message: types.Message):
    global ID
    ID = message.from_user.id
    await bot.send_message(message.from_user.id, 'Выберите команду для изменения меню', reply_markup=admin_kb.button_case_admin)
    await message.delete()

"""Начало диалога загрузки нового пункта меню"""
#@dp.message_handler(commands='Загрузить', state=None)
async def cm_start(message : types.Message):
    if message.from_user.id == ID:
        await FSMAdmin.photo.set()
        await message.reply('Прикрепи фото')

#@dp.message_handler(state='*', commands='отменить')
#@dp.message_handler(Text(equals='отменить', ignore_case=True), state='*')
async def cancel_handler(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        current_state = await state.get_state()
        if current_state is None:
            return
        await state.finish()
        await message.reply('Операция отменена')

"""Ловим первый ответ и пишем в словарь"""
#@dp.message_handler(content_types=['photo'],state=FSMAdmin.photo)
async def load_photo(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['photo'] = message.photo[0].file_id
        await FSMAdmin.next()
        await message.reply("Введи название")

"""Получаем второй ответ и переводим бота в ожидание"""
#@dp.message_handler(state=FSMAdmin.name)
async def load_name(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['name'] = message.text
        await FSMAdmin.next()
        await message.reply('Введи описание')

#@dp.message_handler(state=FSMAdmin.description)
async def load_description(message: types.Message, state: FSMContext):
    if message.from_user.id == ID:
        async with state.proxy() as data:
            data['description'] = message.text
        await FSMAdmin.next()
        await  message.reply('Введи стоимость')

#@dp.message_handler(state=FSMAdmin.price)
async def load_price(message: types.Message, state: FSMContext):
        if message.from_user.id == ID:
            async with state.proxy() as data:
                data['price'] = float(message.text)

            await sqlite_db.sql_add_command(state)

            await state.finish()
@dp.callback_query_handler(lambda x: x.data and x.data.startswith('del '))
async def del_callback_run(callback_query: types.CallbackQuery):
    await sqlite_db.sql_delete_command(callback_query.data.replace('del ', ''))
    await callback_query.answer(text=f'{callback_query.data.replace("del ", "")}Удалена', show_alert=True)

@dp.message_handler(commands="Удалить")
async def delete_item(message: types.Message):
    if message.from_user.id == ID:
        read = await sqlite_db.sql_read2()
        for ret in read:
            await bot.send_photo(message.from_user.id, ret[0], f'{ret[1]}\nОпсание: {ret[2]}\nЦена: {ret[-1]}')
            await bot.send_message(message.from_user.id, text="^^^", reply_markup=InlineKeyboardMarkup().\
                add(InlineKeyboardButton(f'Удалить{ret[1]}', callback_data=f'del {ret[1]}')))

"""Регистрируем Хендлеры"""
def register_handlers_admin(dp : Dispatcher):
    dp.register_message_handler(cm_start, commands=['Загрузить'], state=None)
    dp.register_message_handler(cancel_handler, state='*', commands='отменить')
    dp.register_message_handler(cancel_handler, Text(equals='отменить',ignore_case=True),state='*')
    dp.register_message_handler(load_photo, content_types=['photo'], state=FSMAdmin.photo)
    dp.register_message_handler(load_name, state=FSMAdmin.name)
    dp.register_message_handler(load_description, state=FSMAdmin.description)
    dp.register_message_handler(load_price, state=FSMAdmin.price)
    dp.register_message_handler(make_change_comand, commands=['moderator'], is_chat_admin=True)
    # dp.register_callback_query_handler(del_callback_run, lambda x: x.data and x.data.startswith('del '))
    # dp.register_message_handler(delete_item, commands="Удалить")
