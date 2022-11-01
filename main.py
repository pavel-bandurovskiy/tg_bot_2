from aiogram.utils import executor
from create_bot import dp
from data_base import sqlite_db

async def on_startup():
    print('Бот онлайн')
    sqlite_db.sql_start()

from handlers import client,admin,other

client.registor_handlers_client(dp)
admin.register_handlers_admin(dp)
other.registor_handlers_other(dp)


executor.start_polling(dp)#, on_startup=on_startup)
#executor.start_polling(dp, skip_updates=True)
