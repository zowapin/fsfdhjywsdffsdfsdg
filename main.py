# BOT MADE BY ENCER
#  THANK FOR USING
from middleware import setup_middleware
from handlers import register_handlers
from config.bot_data import dp
from aiogram import executor
import logging

logging.basicConfig(level=logging.INFO)


async def on_startup(_):
    setup_middleware(dp)
    logging.info("-_-_- BOT MADE BY ENCER -_-_-")

register_handlers(dp)

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
