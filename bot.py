import asyncio
from distutils.command.config import config
import os

from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import BotCommand
from aiogram.utils.executor import start_webhook

from data.config import BOT_TOKEN, ADMINS, HEROKU_APP_NAME
import logging

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from handlers.reg_all import reg_all_handlers
from handlers.commands import set_commands
from misc.admin import notify_admin


token = BOT_TOKEN
bot = Bot(BOT_TOKEN, parse_mode=types.ParseMode.HTML)
dp = Dispatcher(bot, storage=MemoryStorage())
logging.basicConfig(level=logging.INFO)
scheduler = AsyncIOScheduler(timezone="Europe/Moscow")
logger = logging.getLogger(__name__)



# def timer_interval_func():
#     """
#     Запускает функцию time_cycle, каждые 60 секунд
#     """
#     scheduler.add_job(time_cycle, "interval", seconds=60, args=(dp,))


HEROKU = HEROKU_APP_NAME

# webhook settings
WEBHOOK_HOST = f'https://{HEROKU}.herokuapp.com'
WEBHOOK_PATH = f'/webhook/{token}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'

# webserver settings
WEBAPP_HOST = '0.0.0.0'
WEBAPP_PORT = os.getenv('PORT', default=8000)

async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL, drop_pending_updates=True)


async def on_shutdown(dispatcher):
    await bot.delete_webhook()


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
    # await dp.start_polling()



  


if __name__ == '__main__':
    asyncio.run(main())
    # start
    start_webhook(
        dispatcher=dp,
        webhook_path=WEBHOOK_PATH,
        skip_updates=True,
        on_startup=on_startup,
        on_shutdown=on_shutdown,
        host=WEBAPP_HOST,
        port=WEBAPP_PORT,
    )
