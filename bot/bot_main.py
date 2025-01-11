from config_file import config  # хуй пойми как оно сработало с импортом
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from bot.handlers import commands, text_messages
from bot.globals import database

async def main():
    # main objects
    database.init()
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    # ---

    # подключаем роутеры к диспетчеру
    dp.include_router(commands.router)
    dp.include_router(text_messages.router)

    # # Регистрируем хендлеры
    # setup_handlers(dp)

    # Устанавливаем команды бота
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь"),
    ])

    # Запускаем long polling
    await dp.start_polling(bot)

if __name__ == "__main__":
    print('start')
    asyncio.run(main())
