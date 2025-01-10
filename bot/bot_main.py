from config_file import config  # хуй пойми как оно сработало с импортом
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from bot.handlers import commands


async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()
    # подключаем роутер к диспетчеру
    dp.include_router(commands.router)
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
    asyncio.run(main())
