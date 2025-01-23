import re


"""
В этом модуле содержатся функции для обработки текста и работы с массивами
"""


def preparing_array_tuple2dict(array: list[tuple]) -> list[dict] or None:
    if not array:
        return array
    result = []
    for item in array:
        result.append(
            {
                'word_en': item[0],
                'word_ru': item[1],
                'pos_en':  item[2],
                'pos_ru': item[3],
                'freq': item[4]

            }
        )
    return result


def detect_language(text):
    # проверка на наличие только букв и пробелов
    if not re.match("^[а-яА-Яa-zA-Z]*$", text):
        return False

    # проверка, является ли текст русским
    if any('\u0400' <= char <= '\u04FF' for char in text):
        return "ru"

    # проверка, является ли текст английским
    if any('a' <= char.lower() <= 'z' for char in text):
        return "en"

    # Если текст пустой или не содержит букв
    return False


def grouping_array_by_pos(word_details: list[dict], lang: str = 'en') -> dict or None:
    """
    :return
    {   'word': str,
        'lang': str,
        "translations":
            [
                {
                    "pos_en": 'str',
                    "pos_ru": 'str',
                    'words_list': [
                                        {'word': str, freq': int}
                                        {...},
                                        ...
                                      ]
                },
                {...}, ..
            ]
    }
    """
    # Проверяет валидность аргумента <lang>
    if lang not in ['en', 'ru']:
        raise ValueError("Argument <lang> is not valid. It must be in ['en', 'ru']")
    if not word_details:
        return
    try:
        word_main = word_details[0][f'word_{lang}']
    except KeyError as _ex:
        print(_ex)
        return
    except IndexError as _ex:
        print(_ex)
        return

        # Фильтрует по убыванию "freq"
    word_details.sort(key=lambda x: x['freq'], reverse=True)

    # Определяем язык перевода
    transl_lang = 'ru' if lang == 'en' else 'en'

    # Группируем данные
    grouped = {}
    for item in word_details:
        pos_en = item['pos_en']
        pos_ru = item['pos_ru']
        word = item[f'word_{transl_lang}']
        freq = item['freq']

        if pos_en not in grouped:
            grouped[pos_en] = {
                'pos_en': pos_en,
                'pos_ru': pos_ru,
                'words_list': []
            }

        grouped[pos_en]['words_list'].append({'word': word, 'freq': freq})

    # Преобразуем словарь в список
    translation = list(grouped.values())
    result = {
        'word': word_main,
        'lang': lang,
        'translations': translation
    }
    return result


def frequency_word(freq: int) -> str:
    if freq == 1:
        return 'редко'
    elif freq in range(2, 5):
        return 'нечасто'
    elif freq in range(5, 11):
        return 'часто'
    else:
        return 'оч. часто'
