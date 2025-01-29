from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def kb_with_answer_options(words) -> ReplyKeyboardMarkup:
    if len(words) != 4:
        raise ValueError('len(words)!= 4 in kb_with_answer_options!')
    keyboard = ReplyKeyboardMarkup(keyboard=[
        [KeyboardButton(text=words[0]), KeyboardButton(text=words[1])],
        [KeyboardButton(text=words[2]), KeyboardButton(text=words[3])]
    ], resize_keyboard=True, one_time_keyboard=True)

    return keyboard
