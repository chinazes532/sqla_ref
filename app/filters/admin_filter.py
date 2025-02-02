import datetime

from aiogram.types import Message

from aiogram.filters import Filter

from app.database.requests.user.add import set_user

import app.keyboards.reply as rkb

from config import ADMINS, BOT_USERNAME


class AdminProtect(Filter):
    def __init__(self):
        self.admins = ADMINS

    async def __call__(self, message: Message):
        return message.from_user.id in self.admins


async def check_start_admin(message: Message, tg_id, current_time):
    await message.answer(f"{message.from_user.full_name.capitalize()}, добро пожаловать в бот!")

    await message.answer("Вы успешно авторизовались как администратор!",
                         reply_markup=rkb.admin_menu)

    await set_user(
        tg_id=tg_id,
        first_name=message.from_user.first_name,
        ref_link=f"https://t.me/{BOT_USERNAME}?start={tg_id}",
        invited_by=None,
        ref_count=0,
        balance=0,
        date=current_time
    )
