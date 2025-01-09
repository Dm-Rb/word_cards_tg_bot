from aiogram import Router
from aiogram.types import Message

# Импортируем функцию или объект для работы с базой данных
from bot.services.database import check_and_add_user

# Создаем роутер для регистрации хендлеров
router = Router()

@router.message(commands=["start"])
async def command_start_handler(message: Message):
    user_id = message.from_user.id  # Получаем ID пользователя

    # Передаем ID пользователя в функцию, которая проверяет наличие в базе
    is_new_user = await check_and_add_user(user_id)  # Ожидаем ответа от функции

    if is_new_user:  # Если пользователя нет в базе (True)
        await message.answer(
            f"Привет, {message.from_user.first_name}! 👋\n"
            "Добро пожаловать! Я помогу тебе изучать английские слова методом интервального повторения."
        )
    # Если пользователя уже нет в базе (False), ничего не делаем