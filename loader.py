import asyncio

from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from utils.db_api.db_gino import db

from data import config

bot = Bot(token=config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
loop = asyncio.get_event_loop()
dp = Dispatcher(bot, storage=storage, loop=loop)

__all__ = ["bot", "storage", "dp", "db"]
