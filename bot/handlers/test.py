from aiogram import Router, F
from aiogram.types import Message
# from bot.services.database import check_word  # Импорт функции проверки слова
from bot.keyboards.inline import get_kb__yes_no_answer  # Импорт функции для клавиатуры

# Создаём роутер
router = Router()

@router.message(F.text)  # Хендлер срабатывает на любое текстовое сообщение
async def word_handler(message: Message):
    word = message.text.strip()  # Получаем отправленное слово
    # word_info = await check_word(word)  # Вызываем функцию для проверки слова



    # Текст из функции check_word
    reply_text = f"{word}\nДобавить в ваш словарь?"

    # Используем клавиатуру из inline.py
    keyboard = get_kb__yes_no_answer(word)

    # Отправляем сообщение с клавиатурой
    await message.answer(reply_text, reply_markup=keyboard)