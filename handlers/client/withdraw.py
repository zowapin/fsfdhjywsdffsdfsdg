from config.bot_data import db, money_name, min_withdraw, min_referrer_withdraw, redirect_link
from utils.message_utils import text_editor
from aiogram import types, Dispatcher
from config.bot_text import text
from markups import cb
import markups as nav


async def withdraw(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "withdraw":
        client_data = await db.get_client_date(call.from_user.id, ("balance",))
        client_referrals = await db.count_referrals(call.from_user.id)
        if client_data[0] < min_withdraw:
            await call.answer(text.no_money.format(money_name=money_name, min_withdraw=min_withdraw), show_alert=True)
            return
        if client_referrals < min_referrer_withdraw:
            await call.answer(text.no_referrals.format(referral=min_referrer_withdraw - client_referrals), show_alert=True)
            return
        await text_editor(text=text.withdraw.format(link=redirect_link), call=call, markup=nav.back_button("main_menu"))

def register_handler_client_withdraw(dp: Dispatcher):
    dp.register_callback_query_handler(withdraw, cb.filter(action=["withdraw"]))