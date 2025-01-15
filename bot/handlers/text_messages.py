from aiogram import Router, F
from aiogram.types import Message
from bot.keyboards.inline import get_kb__yes_no_answer
from bot.globals import database
from bot.services.utils import detect_language, grouping_array_by_pos, preparing_array_tuple2dict
from bot.templates.text import word_details as preparing_message
from bot.services.api_clients import ya_dict_api


router = Router()


@router.message(F.text)  # Хендлер срабатывает на любое текстовое сообщение
async def user_word_handler(message: Message):
    """
    Допилить обработку API на русском!!!
    """
    word = message.text.strip().lower()  # Получаем отправленное слово
    lang = detect_language(word)

    if not lang:
        await message.answer("🙅‍♂️ Cтрока содержит недопустимые символы (цифры, спецсимволы и т.д.)")
        return
    # Получить id, если это слово есть в базе данных
    word_id = await database.get_row_id_by_value_from_table__words(word, lang)
    # Слово присутствует в БД.
    if word_id:
        # Извлекает все связанные данные c <word>
        word_details: list[tuple] = await database.get_translations_word_by_id(word_id, lang)
        if not word_details:
            await message.answer("Что то пошло не так, неопределённая ошибка")
            return
        # Проверяет, есть ли слово в личном словаре ТГ-Юзера
        word_in_table_flag = await database.is_word_in_table__user_data_by_user_id(message.from_user.id, word_id)
        # преобразует ответ из бд (список кортежей) в список словарей (тупо добавляет ключи к значениям)
        word_details: list[dict] = preparing_array_tuple2dict(word_details)
        # Преобразует список словарей в словарь. Группировка по частям речи (стакает переводы по частям речи)
        word_details: dict = grouping_array_by_pos(word_details, lang)
        # Генерирует текст на базе шаблона
        await message.answer(text=preparing_message(word_details, lang), parse_mode='HTML')

        # # Сообщение с инлайн клавиатурой
        if word_in_table_flag:
            reply_text = f"<b>{word.capitalize()}</b> уже добавлено в ваш словарь.\nУбрать из словаря?"
        else:
            reply_text = f"<b>{word.capitalize()}</b>\nДобавить в ваш словарь для изучения?"

        await message.answer(text=reply_text, parse_mode='HTML', reply_markup=get_kb__yes_no_answer(word))

    # Слово отсутствует в БД, делаем запрос к API Yandex Dictionary
    else:
        # Запрос к APi
        ya_dict_api_resp = await ya_dict_api.get_word_details_from_ya_dict(word, lang)
        # Если пустой ответ
        if not ya_dict_api_resp:
            await message.answer("🤷 Слово не найдено, возможно при вводе была допущена опечатка")
            return
        #Добавляет ответ ya_dict_api_resp в БД
        for item in ya_dict_api_resp:
            await database.add_new_couple_to_table__translation_en_ru(
                item['word_en'], item['word_ru'], item['pos_en'], item['freq']
            )
        word_id = await database.get_row_id_by_value_from_table__words(word, lang)
        if not word_id:
            return
        # Проверяет, есть ли слово в личном словаре ТГ-Юзера
        word_in_table_flag = await database.is_word_in_table__user_data_by_user_id(message.from_user.id, word_id)

        # Преобразует список словарей в словарь. Группировка по частям речи (стакает переводы по частям речи)
        # для красивого отображения в мессаге
        word_details: dict = grouping_array_by_pos(ya_dict_api_resp, lang)

        await message.answer(text=preparing_message(word_details, lang), parse_mode='HTML')
        # # Сообщение с инлайн клавиатурой
        if word_in_table_flag:
            reply_text = f"<b>{word.capitalize()}</b> уже добавлено в ваш словарь.\nУбрать из словаря?"
        else:
            reply_text = f"<b>{word.capitalize()}</b>\nДобавить в ваш словарь для изучения?"

        await message.answer(text=reply_text, parse_mode='HTML', reply_markup=get_kb__yes_no_answer(word))

