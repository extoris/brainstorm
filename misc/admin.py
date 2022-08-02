import logging
from aiogram import Dispatcher
from data.config import ADMINS


async def notify_admin(dp: Dispatcher):
    for admin in ADMINS:
        try:
            await dp.bot.send_message(admin, "Бот Запущен")

        except Exception as err:
            logging.exception(err)