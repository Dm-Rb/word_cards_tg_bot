from config_file import config
import asyncio
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from bot.handlers import commands, messages, callbacks, states
from bot.globals import database


async def main():
    # main objects
    database.init()
    bot = Bot(token=config.BOT_TOKEN)
    dp = Dispatcher()

    # ---

    # подключаем роутеры к диспетчеру
    dp.include_router(commands.router)
    dp.include_router(states.router)
    dp.include_router(messages.router)
    dp.include_router(callbacks.router)



    # # Регистрируем хендлеры
    # setup_handlers(dp)

    # Устанавливаем команды бота
    await bot.set_my_commands([
        BotCommand(command="start", description="Запустить бота"),
        BotCommand(command="help", description="Помощь"),
        BotCommand(command='training', description='Тренировать слова')
    ])

    # Запускаем long polling
    try:
        await dp.start_polling(bot)
    finally:
        # Закрываем API клиент после завершения работы
        await bot.session.close()


if __name__ == "__main__":
    print('start')
    asyncio.run(main())
