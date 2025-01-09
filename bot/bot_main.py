from config_file import config  # хуй пойми как оно сработало с импортом
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
# from bot.config import config
# from bot.handlers import setup_handlers

async def main():
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

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
