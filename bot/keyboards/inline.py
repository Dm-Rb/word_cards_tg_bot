from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_kb__yes_no_answer(message: str) -> InlineKeyboardMarkup:
    """
    Создаёт инлайн-клавиатуру с кнопками "ДА" и "НЕТ" для слова.
    :param word: Слово, для которого создаётся клавиатура.
    :return: Объект InlineKeyboardMarkup.
    """
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text="ДА", callback_data=f"add_word:{message}"),
                InlineKeyboardButton(text="НЕТ", callback_data=f"skip_word:{message}"),
            ]
        ]
    )