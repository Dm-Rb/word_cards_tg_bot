from bot.services.database import DataBase

"""
Что бы избежать кругового импорта и в целом геммороя, объект базы данных вынесен в текущий модуль, 
из которого он импортиться куда угодно без головняков
"""
database = DataBase(path='..')
