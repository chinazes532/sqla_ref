import datetime

from aiogram import Router, Bot, F
from aiogram.filters import CommandStart, Command, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

import app.keyboards.reply as rkb
import app.keyboards.inline as ikb
import app.keyboards.builder as bkb

from app.filters.admin_filter import AdminProtect, check_start_admin

from app.database.requests.user.add import set_user
from app.database.requests.user.update import increment_referral_count
from app.database.requests.user.select import get_user, check_referral
from app.filters.user_filter import start_user


user = Router()


@user.message(CommandStart())
async def start_command(message: Message, bot: Bot, command: CommandObject):
    admin = AdminProtect()
    tg_id = message.from_user.id
    ref_link = command.args
    current_time = datetime.datetime.now().strftime("%d.%m.%Y")

    if await admin(message):
        await check_start_admin(message, tg_id, current_time)

        return

    await start_user(
        message, tg_id, current_time,
        bot, ref_link
    )



