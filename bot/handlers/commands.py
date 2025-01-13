from aiogram import Router, F
from aiogram.types import Message
from bot.templates import text
from bot.globals import database


# Импортируем функцию или объект для работы с базой данных
# Создаем роутер для регистрации хендлеров
router = Router()


@router.message(F.text.startswith("/start"))
async def command_start_handler(message: Message):
    user_id = message.from_user.id  # Получаем ID пользователя

    # # Передаем ID пользователя в функцию, которая проверяет наличие в базе возвращает t\f. Подставить в is_new_user
    is_new_user = await database.check_user_in_table(user_id)
    print(is_new_user)
    #
    if not is_new_user:  # Если пользователя нет в базе (False)
        await database.add_new_user(user_id)
        await message.answer(
            text.start_command_new_user(message.from_user.first_name)
        )
    else:
        await message.answer(
            text.start_command_user(message.from_user.first_name)
        )
    # Если пользователя уже нет в базе (False), ничего не делаем


