import logging

from aiogram import Dispatcher, Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from config.config_reader import load_config

storage = MemoryStorage()

logger = logging.getLogger(__name__)

config = load_config(r'D:\Users\Tim\Desktop\pycharmprojects\Diary_bot\config\config.ini')

TOKEN = config.tg_bot.BOT_TOKEN

bot = Bot(TOKEN)

dp = Dispatcher(bot, storage=storage)
