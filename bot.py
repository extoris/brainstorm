import asyncio

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand

from data.config import BOT_TOKEN, ADMINS
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.reg_all import reg_all_handlers
from handlers.commands import set_commands
from misc.admin import notify_admin

bot = Bot(token=BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
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
    await dp.start_polling()


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.error("Bot stopped!")