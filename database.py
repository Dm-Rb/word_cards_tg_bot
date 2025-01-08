import aiosqlite
import sqlite3


class DataBaseWords:

    def __init__(self, db_name: str = 'words.db'):
        self.db_name = db_name
        # create tables if it not exist
        self.create_tables()

    #  START create main tables BLOCK

    def __create_table_words_en(self):
        """
        id -> PRIMARY KEY
        word_en -> слово или словосочетание en
        noun -> флаг, является ли данная запись существительным, значения 1 или 0 (NULL)
        verb -> флаг, является ли данная запись глаголом, значения 1 или 0 (NULL)
        adjective -> флаг, является ли данная запись прилагательным, значения 1 или 0 (NULL)
        :return:
        """
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS words_en (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word_en TEXT UNIQUE NOT NULL,
                    noun INTEGER, 
                    verb INTEGER,
                    adjective INTEGER
                )
            ''')
            conn.commit()

    def __create_table_words_ru(self):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS words_ru (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word_ru TEXT UNIQUE NOT NULL,
                    noun INTEGER, 
                    verb INTEGER,
                    adjective INTEGER
                )
            ''')
            conn.commit()

    def __create_table_translation_en_ru(self):
        """
        id_words_en -> ссылка на words_en.id
        id_word_ru -> ссылка на words_ru.id
        frequency - > частота употребления в данном контексте/переводе, числовое значение        
        """""
        with sqlite3.connect(self.db_name) as conn:
            conn.execute('''
                CREATE TABLE IF NOT EXISTS translation_en_ru (
                    id_word_en INTEGER NOT NULL,
                    id_word_ru INTEGER NOT NULL,
                    frequency INTEGER,
                    FOREIGN KEY (id_word_en) REFERENCES words_en(id),
                    FOREIGN KEY (id_word_ru) REFERENCES words_ru(id)
                )
            ''')
            conn.commit()

    def create_tables(self):
        self.__create_table_words_en()
        self.__create_table_words_ru()
        self.__create_table_translation_en_ru()

    # END create main tables BLOCK

    #  START operations with main tables BLOCK

    async def add_new_row_to__words_en(self, word: str, n: int = 0, v: int = 0, a: int = 0) -> int:
        """
        Добавляет запись (если её нет), возвращает ID.
        word:
        :return: ID строки.
        """
        async with aiosqlite.connect(self.db_name) as db:
            # попробуем вставить новую запись. если идентичная строка уже есть - скипаем
            await db.execute(
                'INSERT OR IGNORE INTO words_en (word_en, noun, verb, adjective) VALUES (?, ?, ?, ?)',
                (word, n, v, a, )
            )
            await db.commit()

            # получаем ID строки
            async with db.execute('SELECT id FROM words_en WHERE word_en = ?', (word,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return row[0]
                else:
                    raise Exception(f"Ошибка при получении id, таблицы words_en, базы данных {self.db_name}")

    async def add_new_row_to__words_ru(self, word: str) -> int:
        """
        Добавляет запись, если её нет, и  возвращает ID.
        :return: ID строки.
        """
        async with aiosqlite.connect(self.db_name) as db:
            # попробуем вставить новую запись. если идентичная строка уже есть - скипаем
            await db.execute(
                'INSERT OR IGNORE INTO words_ru (word_ru) VALUES (?)',
                (word, )
            )
            await db.commit()

            # получаем ID строки
            async with db.execute('SELECT id FROM words_ru WHERE word_ru = ?', (word,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return row[0]
                else:
                    raise Exception(f"Ошибка при получении id, таблицы words_ru, базы данных {self.db_name}")

    async def add_new_couple_en_ru(self, word_en: str, word_ru: str, n=0, v=0, a=0, freq=5):
        id_word_en = await self.add_new_row_to__words_en(word_en, n, v, a)
        id_word_ru = await self.add_new_row_to__words_ru(word_ru)
        async with aiosqlite.connect(self.db_name) as db:
            # попробуем вставить новую запись. если идентичная строка уже есть - скипаем
            await db.execute(
                'INSERT INTO translation_en_ru (id_word_en, id_word_ru, frequency) VALUES (?, ?, ?)',
                (id_word_en, id_word_ru, freq, )
            )
            await db.commit()

    #  END operations with main tables BLOCK
# async def main():
#     db = DataBaseWords()
#
#     # d = await db.add_new_couple_en_ru("fex", 'чтото', 0, 1, 0, 10)
#     await db.add_new_couple_en_ru("fex",'чтото', 0, 1, 0, 15)
#
# if __name__ == "__main__":
#
#     import asyncio
#     asyncio.run(main())
