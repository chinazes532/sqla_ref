from aiogram import Bot
from aiogram.types import Message

from app.database.requests.user.add import set_user
from app.database.requests.user.select import check_referral
from app.database.requests.user.update import increment_referral_count

from config import BOT_USERNAME


async def start_user(
        message: Message, tg_id, current_time,
        bot: Bot, ref_link
    ):
    user_registered = await set_user(
        tg_id=tg_id,
        first_name=message.from_user.first_name,
        ref_link=f"https://t.me/{BOT_USERNAME}?start={tg_id}",
        invited_by=None,
        ref_count=0,
        balance=0,
        date=current_time
    )

    if user_registered:
        if ref_link:
            invited_by = await check_referral(ref_link)
            if invited_by:
                await set_user(
                    tg_id=tg_id,
                    first_name=message.from_user.first_name,
                    ref_link=f"https://t.me/{BOT_USERNAME}?start={tg_id}",
                    invited_by=invited_by,
                    ref_count=0,
                    balance=0,
                    date=current_time
                )

                await bot.send_message(
                    chat_id=tg_id,
                    text=f"Вы зарегистрировались на сайте. "
                         f"Вас пригласил пользователь: {invited_by}"
                )

                await bot.send_message(
                    chat_id=invited_by,
                    text=f"Пользователь {tg_id} перешел по вашей реферальной ссылке"
                )

                await increment_referral_count(invited_by)
            else:
                await bot.send_message(
                    chat_id=tg_id,
                    text=f"{message.from_user.full_name.capitalize()}, реферальная ссылка некорректна"
                )
        else:
            await bot.send_message(
                chat_id=tg_id,
                text=f"{message.from_user.full_name.capitalize()}, добро пожаловать в бот!"
            )
    else:
        await bot.send_message(
            chat_id=tg_id,
            text=f"{message.from_user.full_name.capitalize()}, добро пожаловать в бот!"
        )