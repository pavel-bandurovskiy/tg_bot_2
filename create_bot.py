from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from auth_data import tok
from aiogram.contrib.fsm_storage.memory import MemoryStorage

storage = MemoryStorage()

bot = Bot(tok)
dp = Dispatcher(bot, storage = storage)
