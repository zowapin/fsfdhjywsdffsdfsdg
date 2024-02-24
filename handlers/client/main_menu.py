from config.bot_data import db, money_name, bot_username, balance_for_click
from utils.message_utils import text_editor
from asyncio import sleep, create_task
from aiogram import types, Dispatcher
from config.bot_text import text
from markups import cb
import markups as nav


async def click(user_id: int, call: types.CallbackQuery):
    msg = await text_editor(text=text.sleep_message, call=call)
    await sleep(5)
    client_balance = (await db.get_client_date(user_id, ("balance",)))[0]
    await db.update_data(user_id, ("balance", client_balance + balance_for_click))
    await text_editor(text=text.pay_click, call=call, message_id=msg.message_id, markup=nav.clicker_menu)


async def main_commands(call: types.CallbackQuery, callback_data: dict):
    action = callback_data["action"]
    if action == "profile":
        balance = (await db.get_client_date(call.from_user.id, ("balance",)))[0]
        await text_editor(text=text.profile.format(ID=call.from_user.id, username=call.from_user.username,
                                                   balance=round(balance, 1),
                                                   referrer=await db.count_referrals(call.from_user.id)),
                          call=call,
                          markup=nav.back_button("main_menu"))
    elif action == "start":
        await text_editor(text=text.main_menu.format(money_name=money_name),
                          call=call,
                          markup=nav.main_menu(call.from_user.id))
    elif action == "start_earn":
        await text_editor(text=text.earn, call=call, markup=nav.earn_keyboard)
    elif action == "invite_friends":
        await text_editor(text=text.invite.format(link=f"https://t.me/{bot_username}?start={call.from_user.id}"),
                          call=call, markup=nav.back_button("earn_menu"))
    elif action == "clicker":
        await text_editor(text=text.clicker, call=call, markup=nav.clicker_menu)
    elif action == "click":
        create_task(click(call.from_user.id, call))


def register_handler_client_main(dp: Dispatcher):
    dp.register_callback_query_handler(main_commands, cb.filter(action=["profile", "start_earn", "start",
                                                                        "invite_friends", "clicker", "click"]))