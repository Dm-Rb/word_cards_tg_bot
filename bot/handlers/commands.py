from aiogram import Router, F
from aiogram.types import Message
from bot.templates import text

# Импортируем функцию или объект для работы с базой данных
# Создаем роутер для регистрации хендлеров
router = Router()


@router.message(F.text.startswith("/start"))
async def command_start_handler(message: Message):
    user_id = message.from_user.id  # Получаем ID пользователя

    # # Передаем ID пользователя в функцию, которая проверяет наличие в базе возвращает t\f. Подставить в is_new_user
    is_new_user = True
    #
    if is_new_user:  # Если пользователя нет в базе (True)
        await message.answer(
            text.start_command(message.from_user.first_name)
        )
    # Если пользователя уже нет в базе (False), ничего не делаем


