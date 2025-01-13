from bot.services.utils import frequency_word


def start_command(user_first_name):
    message = \
        f"""Привет, {user_first_name}! 👋
Добро пожаловать! Этот бот поможет тебе изучать английские слова методом интервального повторения."""

    return message

def word_details(word_details_dict):
    message = ''
    # Правильное закрытие тега <b>
    message += f"<b>{word_details_dict['word'].capitalize()}</b>"
    for item_transl in word_details_dict['translation']:
        # Используем <i> с корректным закрытием </i>
        transl_text = f"\n<i>{item_transl['pos_en']}/{item_transl['pos_ru']}:</i>\n"
        # Формируем список переведенных слов
        transl_text += ', '.join([f"{item['word']} <i>({frequency_word(item['freq'])})</i>" for item in item_transl['words_list']])
        message += '\n' + transl_text
    return message
