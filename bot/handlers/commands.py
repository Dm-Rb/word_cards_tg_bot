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
    is_new_user: bool = await database.check_user_in_table(user_id)
    #
    if not is_new_user:  # Если ID пользователя нет в БД (is_new_user=False)
        await database.add_new_user(user_id)
        await message.answer(
            text.start_command(message.from_user.first_name, is_new_user)
        )
    else:
        await message.answer(
            text.start_command(message.from_user.first_name, is_new_user)
        )
    # Если пользователя уже нет в базе (False), ничего не делаем


