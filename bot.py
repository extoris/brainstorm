import asyncio
from datetime import datetime
from distutils.command.config import config
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.utils.executor import start_webhook

from data.config import BOT_TOKEN, ADMINS
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.reg_all import reg_all_handlers
from handlers.commands import set_commands
from misc.admin import notify_admin


token = BOT_TOKEN
bot = Bot(BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
formatter = '[%(asctime)s] %(levelname)8s --- %(message)s (%(filename)s:%(lineno)s)'
logging.basicConfig(
    filename=f'bot-from-{datetime.now().date()}.log',
    filemode='w',
    format=formatter,
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.WARNING)

scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
logger = logging.getLogger(__name__)


# def timer_interval_func():
#     """
#     Запускает функцию time_cycle, каждые 60 секунд
#     """
#     scheduler.add_job(time_cycle, "interval", seconds=60, args=(dp,))


async def main():
    """
    await bot.delete_webhook(drop_pending_updates=True) - в новых версиях aiogram есть проблема, то что при запуске бота,
        он реагирует на сообщения, которые были отправленны ему, пока он был выключен и это не чинилось dp.skip_updates()
        подробнее об этой ошибке: https://github.com/aiogram/aiogram/issues/418
    """
    # Удаление последнего сообщения
    # await bot.delete_webhook(drop_pending_updates=True)

    # # Это запуск таймера AsyncIOScheduler
    # scheduler.start()
    # # Запуск функции таймера
    # timer_interval_func()

    await set_commands(dp)

    # функция регистрации "register_message_handler"
    await reg_all_handlers(dp)

    await notify_admin(dp)

    # Запуск полинга
    try:
        # disp = Dispatcher(bot=bot)
        # disp.register_message_handler(start_handler, commands={"start", "restart"})
        await dp.start_polling()
    finally:
        await bot.close()
    

if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")
