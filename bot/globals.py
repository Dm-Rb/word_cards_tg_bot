from bot.services.database import DataBase
from pathlib import Path


"""
Что бы избежать кругового импорта и в целом геммороя, объект базы данных вынесен в текущий модуль, 
из которого он импортиться куда угодно без головняков
"""
# Определяем корневую директорию проекта
BASE_DIR = Path(__file__).resolve().parent.parent  # Уровень выше каталога bot
# Создаём объект базы данных с абсолютным путём
database = DataBase(path=BASE_DIR)
