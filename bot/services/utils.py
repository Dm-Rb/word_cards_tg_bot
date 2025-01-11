import re


"""
В этом модуле содержатся функции для обработки текста и работы с массивами
"""


def detect_language(text):
    # проверка на наличие только букв и пробелов
    if not re.match("^[а-яА-Яa-zA-Z ]*$", text):
        return False

    # проверка, является ли текст русским
    if any('\u0400' <= char <= '\u04FF' for char in text):
        return "ru"

    # проверка, является ли текст английским
    if any('a' <= char.lower() <= 'z' for char in text):
        return "en"

    # Если текст пустой или не содержит букв
    return False
