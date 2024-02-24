from typing import Any, Callable, Coroutine
from aiogram.dispatcher.filters import Text
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery
from aiogram import types, Dispatcher
from itertools import islice


class Paginator:
    def __init__(self,
                 data: types.InlineKeyboardMarkup | types.InlineKeyboardButton,
                 callback_startswith: str = 'page|',
                 size: int = 8,
                 page_separator: str = '/',
                 dp: Dispatcher | None = None,
                 back_callback: str = "main_menu"):
        self.dp = dp
        self._page_separator = page_separator
        self._startswith = callback_startswith
        self._size = size
        self._back_callback = f"back|{back_callback}"
        if isinstance(data, (types.InlineKeyboardMarkup, types.InlineKeyboardButton)):
            self._keyboard_list = list(
                self._chunk(
                    it=data.inline_keyboard,
                    size=self._size
                )
            )
        else:
            raise ValueError(f"{data} is not valid data")

    @staticmethod
    def _chunk(it, size):
        it = iter(it)
        return iter(lambda: tuple(islice(it, size)), ())

    @staticmethod
    def _get_page(call: types.CallbackQuery) -> int:
        return int(call.data[call.data.find("|") + 1:])

    def _get_paginator(self,
                       counts: int,
                       page: int,
                       page_separator: str = '/',
                       startswith: str = 'page|'
                       ) -> list[types.InlineKeyboardButton]:
        counts -= 1
        paginations = []
        if page > 0:
            paginations.append(
                types.InlineKeyboardButton(
                    text='⬅️',
                    callback_data=f'{startswith}{page - 1}'
                ),
            )
        paginations.append(
            types.InlineKeyboardButton(
                text=f'{page + 1}{page_separator}{counts + 1}',
                callback_data='pass'
            ),
        )
        if counts > page:
            paginations.append(
                types.InlineKeyboardButton(
                    text='➡️',
                    callback_data=f'{startswith}{page + 1}'
                )
            )
        return paginations

    def __call__(
            self,
            current_page=0,
            *args,
            **kwargs
    ) -> types.InlineKeyboardMarkup:
        _list_current_page = self._keyboard_list[current_page]
        paginations = self._get_paginator(
            counts=len(self._keyboard_list),
            page=current_page,
            page_separator=self._page_separator,
            startswith=self._startswith
        )
        keyboard = types.InlineKeyboardMarkup(inline_keyboard=[*_list_current_page, paginations]).add(types.InlineKeyboardButton(text="🔙 Назад", callback_data=self._back_callback))
        if self.dp:
            self.paginator_handler()
        return keyboard

    def paginator_handler(self) -> tuple[Callable[[CallbackQuery, FSMContext], Coroutine[Any, Any, None]], Text]:
        async def _page(call: types.CallbackQuery):
            page = self._get_page(call)
            await call.message.edit_reply_markup(
                reply_markup=self.__call__(
                    current_page=page
                )
            )
        if not self.dp:
            return _page, Text(startswith=self._startswith)
        else:
            self.dp.register_callback_query_handler(
                _page,
                Text(startswith=self._startswith),
            )
