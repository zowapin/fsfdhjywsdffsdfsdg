from aiogram.dispatcher.filters.state import StatesGroup, State

class Admin(StatesGroup):
    class AddTask(StatesGroup):
        data = State()
        description = State()
        reward = State()
        task_id = State()

    class DeleteTask(StatesGroup):
        task_id = State()

    class Mailing(StatesGroup):
        get_data = State()
        get_confirm = State()

    class AddPromo(StatesGroup):
        data = State()
        get_promo = State()
        get_reward = State()

    class DeletePromo(StatesGroup):
        get_promo = State()

class Client(StatesGroup):
    class Promo(StatesGroup):
        get_promo = State()
