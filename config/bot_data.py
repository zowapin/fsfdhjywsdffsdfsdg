from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram import Bot, Dispatcher, types
from config.database.data import DataBase
import os

db = DataBase(os.path.join(os.getcwd(), "config", "database", "data.db"))

# _________________________Настройка Бота____________________________
admin_id = []
token = ""
# ___________________________________________________________________

# ___________________________________________________________________
balance_for_referral = 25
balance_for_click = 0.5
money_name = "Gold"
bot_username = "HyperTapX_bot"
min_withdraw = 150
redirect_link = "https://t.me/HyperTapX_bot"
min_referrer_withdraw = 3
feedback_link = "https://t.me/+aa9NjIBBIw9kMDhi"
# ___________________________________________________________________
bot = Bot(token=token, parse_mode=types.ParseMode.HTML)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)
