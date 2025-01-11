from aiogram import Router, F
from aiogram.types import Message
from bot.keyboards.inline import get_kb__yes_no_answer
from bot.globals import database
from bot.services.utils import detect_language

router = Router()


@router.message(F.text)  # Хендлер срабатывает на любое текстовое сообщение
async def user_word_handler(message: Message):
    """
    Допилить!!!
    """
    word = message.text.strip().lower()  # Получаем отправленное слово
    lang = detect_language(word)
    if not lang:
        await message.answer("Введено некорректное значение, не удалось распознать язык")
        return
    # Получить id, если это слово есть в базе данных
    word_id = await database.get_row_id_by_value_from_table__words(word, lang)
    if word_id:
        # Слово присутствует в БД. Иизвлеаем все связанные данные
        items = await database.get_translations_word_by_id(word_id, lang)
        await message.answer(str(items))
    else:
        pass

    # Текст из функции check_word
    reply_text = f"{word}\nДобавить в ваш личный словарь для изучения?"

    # Используем клавиатуру из inline.py
    keyboard = get_kb__yes_no_answer(word)

    # Отправляем сообщение с клавиатурой
    await message.answer(reply_text, reply_markup=keyboard)