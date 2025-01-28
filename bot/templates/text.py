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
        transl_text = f"\n📎 <i>{item_transl['pos_en']}/{item_transl['pos_ru']}:</i>\n"
        # Формируем список переведенных слов
        transl_text += \
            ', '.join([f"{item['word']} <i>({frequency_word(item['freq'])})</i>" for item in item_transl['words_list']])
        message += '\n' + transl_text
    return message


def question_without_context(word, pos_en, pos_ru, random_translation_ru, lang='en'):
    lags_emoji = {'en': '🇬🇧', 'ru': '🇷🇺'}
    message = ''
    message += f"Слово:  <b>{word.capitalize()}</b> {lags_emoji[lang]}\n"
    message += f"⇨ Часть речи:  <i>{pos_en}/{pos_ru}</i>\n"
    if random_translation_ru and len(random_translation_ru) >= 3:
        message += f'⇨ Подсказка:  {random_translation_ru[0].upper()}'\
                   f'{"".join(["*" for _ in range(len(random_translation_ru) - 2)])}' \
                   f'{random_translation_ru[-1].upper()}\n'
    message += '\n🚫 <i>прервать тренировку</i> /break'
    return message


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

