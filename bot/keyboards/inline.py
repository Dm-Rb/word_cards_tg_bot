from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_kb__yes_no_answer(word: str, word_id:int, user_id: int, fuc_type: str) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру с кнопками "ДА" и "НЕТ" для слова.
    :param word: Слово, для которого создаётся клавиатура.
    :return: Объект InlineKeyboardMarkup.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="ДА", callback_data=f"yes:{word}:{str(word_id)}:{str(user_id)}:{fuc_type}"),
                InlineKeyboardButton(text="НЕТ", callback_data=f"no:{word}:{str(word_id)}:{str(user_id)}:{fuc_type}"),
            ]
        ]
    )