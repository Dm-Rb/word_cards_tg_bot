from bot.services.utils import frequency_word


def start_command(user_first_name, is_new_user: bool) -> str:
    if not is_new_user:
        message = \
        f"""Привет, {user_first_name}! 👋
Добро пожаловать! Этот бот поможет тебе изучать английские слова методом интервального повторения."""
    else:
        message = f"""C возвращением, {user_first_name}! 👋"""

    return message


def word_details(word_details_dict, lang):
    lags_emoji = {'en': '🇬🇧', 'ru': '🇷🇺'}
    message = ''
    message += f"<b>{word_details_dict['word'].capitalize()}</b>  {lags_emoji[lang]}"
    for item_transl in word_details_dict['translations']:
        # Используем <i> с корректным закрытием </i>
        transl_text = f"\n⇨ <i>{item_transl['pos_en']}/{item_transl['pos_ru']}:</i>\n"
        # Формируем список переведенных слов
        transl_text += preparing_word_list_item(item_transl['words_list'])
        # transl_text += \
        #     ', '.join([f"{item['word']} <i>({frequency_word(item['freq'])})</i>" for item in item_transl['words_list']])
        message += '\n' + transl_text
    return message

def preparing_word_list_item(data):
    grouped = {}
    for item in data:
        freq = frequency_word(int(item['freq']))
        freq = f"➖<i>({freq})</i>"
        word = item['word']
        if freq not in grouped:
            grouped[freq] = []
        grouped[freq].append(word)

    # # Преобразуем результат в нужный формат
    result = [freq + '\n' + ', '.join(words) for freq, words in grouped.items()]
    result = '\n'.join(result)
    return f"<blockquote>{result}</blockquote>"


def question_without_context(word, pos_en, pos_ru, translation_ru=None, lang='en'):
    # random_translation_ru - это слово-перевод, который будет использоваться в качестве подсказки
    # Если None, то подсказки не будет
    lags_emoji = {'en': '🇬🇧', 'ru': '🇷🇺'}
    message = ''
    message += f"{lags_emoji[lang]} <b>{word.capitalize()}</b>\n"
    message += f"⇨ <i>{pos_en}/{pos_ru}</i>\n"
    if translation_ru:
        message += f'⇨ Подсказка:  {preparing_translation_ru_word(translation_ru)}\n'
    message += '\n🚫 <i>прервать тренировку</i> /break'
    return message


def preparing_translation_ru_word(translation_ru):
    result = ''
    slices = len(translation_ru) // 2
    for i in range(len(translation_ru)):
        if i <= slices:
            result += f'<tg-spoiler>{translation_ru[i]}</tg-spoiler>'
        else:
            if translation_ru[i] != ' ':
                result += '*'
            else:
                result += ' '
    return result


def show_statistic_training(results):
    answers = ''
    wrong_count = 0
    correct_counter = 0
    for item in results:
        if item['answer_is_correct']:
            correct_counter += 1
        else:
            wrong_count += 1
            answers += \
                f"\n🇬🇧️ <b>{item['word'].capitalize()}</b> " \
                f"<i>({item['pos']})</i>\n" \
                f"🔴 ваш ответ: {item['user_answer'].lower()}\n" \
                f"🟢 правильный(е) ответ(ы): {', '.join(item['correct_words'])}\n"

    message = f'✅ Верных ответов: {str(correct_counter)}\n❌ Неверных ответов: {str(wrong_count)}'
    if answers:
        message = message + '\n\nРабота над ошибками:\n' + answers
    return message

