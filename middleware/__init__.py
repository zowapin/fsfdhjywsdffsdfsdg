from aiogram import Dispatcher
from middleware.throttling_middleware import ThrottlingMiddleware

def setup_middleware(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())