from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData
from config.bot_data import admin_id, feedback_link

cb = CallbackData("fabnum", "action")

def welcome_menu(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("🖥 Начать", callback_data=cb.new(action="start")))
    if user_id in admin_id:
        keyboard.add(InlineKeyboardButton("👤 Admin Menu", callback_data=cb.new(action="admin_menu")))
    return keyboard

def main_menu(user_id: int) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(InlineKeyboardButton("💸 Заработать", callback_data=cb.new(action="start_earn")))
    keyboard.row(
        InlineKeyboardButton("👤 Профиль", callback_data=cb.new(action="profile")),
        InlineKeyboardButton("💳 Вывести", callback_data=cb.new(action="withdraw")))
    keyboard.add(
        InlineKeyboardButton("🎟 Промокод", callback_data=cb.new(action="enter_promocode"))
    )
    if feedback_link:
        keyboard.add(InlineKeyboardButton("👉 Наши отзывы ⭐️", url=feedback_link))
    if user_id in admin_id:
        keyboard.add(InlineKeyboardButton("👤 Admin Menu", callback_data=cb.new(action="admin_menu")))
    return keyboard

def back_button(value: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("🔙 Назад", callback_data=f"back|{value}")
    )
    return keyboard


earn_keyboard = InlineKeyboardMarkup(row_width=1)
earn_keyboard.add(
        InlineKeyboardButton("💥 Кликер", callback_data=cb.new(action="clicker")),
        InlineKeyboardButton("💰 Задания", callback_data=cb.new(action="tasks")),
        InlineKeyboardButton("👥 Пригласить друзей", callback_data=cb.new(action="invite_friends")),
        InlineKeyboardButton("🔙 Назад", callback_data="back|main_menu")
)


clicker_menu = InlineKeyboardMarkup(row_width=1)
clicker_menu.add(
        InlineKeyboardButton("💥 Клик", callback_data=cb.new(action="click")),
        InlineKeyboardButton("🔙 Назад", callback_data="back|earn_menu")
)


def complete_task_menu(value: str) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(row_width=1)
    keyboard.add(
        InlineKeyboardButton("✅ Проверить", callback_data=f"check|{value}"),
        InlineKeyboardButton("🔙 Назад", callback_data="back|earn_menu")
    )
    return keyboard


admin_menu = InlineKeyboardMarkup(row_width=2)
admin_menu.add(InlineKeyboardButton("🖋 Создать рассылку", callback_data=cb.new(action="mailing_menu"))).row()
admin_menu.add(
        InlineKeyboardButton("➕ Добавить задание", callback_data=cb.new(action="add_task")),
        InlineKeyboardButton("➖ Удалить задание", callback_data=cb.new(action="delete_task")),
        InlineKeyboardButton("🎟 Создать промокод", callback_data=cb.new(action="create_promo")),
        InlineKeyboardButton("➖ Удалить промокод", callback_data=cb.new(action="delete_promo")),
        InlineKeyboardButton("📃 Статистика", callback_data=cb.new(action="statistic"))
).row()
admin_menu.add(InlineKeyboardButton("🔙 Назад", callback_data="back|main_menu"))


add_task_menu = InlineKeyboardMarkup(row_width=2)
add_task_menu.add(
        InlineKeyboardButton("📃 Описание", callback_data=cb.new(action="change_description")),
        InlineKeyboardButton("💵 Вознаграждение", callback_data=cb.new(action="change_reward")),
        InlineKeyboardButton("🆔 Канала", callback_data=cb.new(action="change_channel_id"))
).row()
add_task_menu.add(InlineKeyboardButton("📤 Опубликовать задание", callback_data=cb.new(action="publish_task"))).row()
add_task_menu.add(InlineKeyboardButton("🔙 Назад", callback_data="back|admin_menu"))


confirm_menu = InlineKeyboardMarkup(row_width=1)
confirm_menu.add(
                 InlineKeyboardButton("✅ Подтвердить", callback_data=cb.new(action="confirm")),
                 InlineKeyboardButton("🔙 Назад", callback_data="back|admin_menu")
)


promo_menu = InlineKeyboardMarkup(row_width=2)
promo_menu.add(
        InlineKeyboardButton("🎟 Промокод", callback_data=cb.new(action="enter_promo")),
        InlineKeyboardButton("💵 Вознаграждение", callback_data=cb.new(action="enter_reward")),
        InlineKeyboardButton("📤 Опубликовать промокод", callback_data=cb.new(action="publish_promo"))
).row()
promo_menu.add(InlineKeyboardButton("🔙 Назад", callback_data="back|admin_menu"))



