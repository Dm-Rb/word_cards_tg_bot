import aiosqlite
import sqlite3


class DataBaseWords:

    def __init__(self, db_name: str = 'dictionary.db'):
        self.db_name = db_name
        # create tables if it not exist
        self.create_tables()
        # vars
        self.parts_of_speech_const = self.__get_parts_of_speech_const()

    #  START create main tables BLOCK

    def __create_table__words(self, lang: str):

        with sqlite3.connect(self.db_name) as conn:
            conn.execute(
                f'''
                CREATE TABLE IF NOT EXISTS words_{lang} (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    word TEXT UNIQUE NOT NULL
                )
                '''
            )
            conn.commit()

    def __create_table__parts_of_speech_const(self):
        """
        Эта таблица содержит константы id, на которые ссылается таблица relationships. Строго три значения
        """
        with sqlite3.connect(self.db_name) as conn:
            conn.execute(
                f'''
                CREATE TABLE IF NOT EXISTS parts_of_speech_const(
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    pos_en TEXT UNIQUE NOT NULL,
                    pos_ru TEXT UNIQUE NOT NULL                    
                )
                '''
            )
            conn.commit()
            for pos_en, pos_ru in zip(['noun', 'verb', 'adjective'], ['существительное', 'глагол', 'прилагательное']):
                conn.execute(
                    "INSERT OR IGNORE INTO parts_of_speech_const (pos_en, pos_ru) VALUES (?, ?)",
                    (pos_en, pos_ru, )
                             )
                conn.commit()
    def __get_parts_of_speech_const(self) -> dict:
        with sqlite3.connect(self.db_name) as conn:
            r = conn.execute('SELECT * FROM parts_of_speech_const').fetchall()
            if not r:
                raise Exception(f"Ошибка при получении значений таблицы {self.db_name}.parts_of_speech_const")
            result = {}
            for item in r:
                result[item[1]] = {'id': item[0], 'ru': item[2]}
            return result



    def __create_table__translation_en_ru(self):

        with sqlite3.connect(self.db_name) as conn:
            conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS translation_en_ru (
                    id_word_en INTEGER NOT NULL,
                    id_word_ru INTEGER NOT NULL,
                    id_pos INTEGER NOT NULL,
                    frequency INTEGER,
                    FOREIGN KEY (id_word_en) REFERENCES words_en(id),
                    FOREIGN KEY (id_word_ru) REFERENCES words_ru(id),
                    FOREIGN KEY (id_pos) REFERENCES parts_of_speech_const(id)
                )
                '''
            )
            conn.commit()

    def create_tables(self):
        [self.__create_table__words(lang) for lang in ['en', 'ru']]
        self.__create_table__parts_of_speech_const()
        self.__create_table__translation_en_ru()

    #  END create main tables BLOCK
    ####
    #  START operations with main tables BLOCK

    async def __add_new_row_to_table__words(self, word: str, lang: str) -> int:
        """
        Добавляет запись (если её нет), возвращает ID.
        word:
        :return: ID строки.
        """
        if lang not in ['en', 'ru']:
            raise ValueError("Argument <lang> is not valid. It must be in ['en', 'ru']")

        async with aiosqlite.connect(self.db_name) as conn:
            # попробуем вставить новую запись. если идентичная строка уже есть - скипаем
            await conn.execute(
                f'INSERT OR IGNORE INTO words_{lang} (word) VALUES (?)',
                (word, )
            )
            await conn.commit()

            # получаем ID строки
            async with conn.execute(f'SELECT id FROM words_{lang} WHERE word = ?', (word,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return row[0]
                else:
                    raise Exception(f"Ошибка при получении id, таблицы words_{lang}, базы данных {self.db_name}")

    async def add_new_couple_to_table__translation_en_ru(self, word_en: str, word_ru: str, pos: str, freq: int):
        id_word_en = await self.__add_new_row_to_table__words(word_en, 'en')
        id_word_ru = await self.__add_new_row_to_table__words(word_ru, 'ru')
        try:
            id_pos = self.parts_of_speech_const[pos]['id']
        except KeyError:
            print(f'ключ {pos} не содержится в аттрибуте <parts_of_speech_const>')
            raise KeyError

        async with aiosqlite.connect(self.db_name) as db:
            # попробуем вставить новую запись. если идентичная строка уже есть - скипаем
            await db.execute(
                'INSERT INTO translation_en_ru (id_word_en, id_word_ru, id_pos, frequency) VALUES (?, ?, ?, ?)',
                (id_word_en, id_word_ru, id_pos, freq,)
            )
            await db.commit()

db = DataBaseWords()

