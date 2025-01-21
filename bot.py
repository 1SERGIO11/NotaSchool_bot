import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

from venv import BOT_TOKEN
from handler import common, start, introduction, payment

bot = Bot(token=BOT_TOKEN)

async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    )

    dp = Dispatcher(storage=MemoryStorage())
    await bot.set_my_commands([
        BotCommand(command="start", description="Начало работы с ботом")
    ])

    dp.include_router(common.router)
    dp.include_router(start.router)
    dp.include_router(introduction.router)
    dp.include_router(payment.router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())