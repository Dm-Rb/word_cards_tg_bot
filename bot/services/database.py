import aiosqlite
import sqlite3
from os.path import join as join_path

class DataBaseDictionary:

    def __init__(self, db_name: str = 'dictionary.db', db_path='files'):
        self.db_path = join_path(db_path, db_name)
        # create tables if it not exist
        self.__create_tables()
        # vars
        self.parts_of_speech_const = self.__get_parts_of_speech_const()

    #  START create main tables BLOCK

    def __create_table__words(self, lang: str):
        """
        Таблица для слов, ангийских и русских (окончание в названии указывает на содержание)
        """

        with sqlite3.connect(self.db_path) as conn:
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
        Таблица содержит названия частей речи, генерируется статично при инициализации
        """
        with sqlite3.connect(self.db_path) as conn:
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
            for pos_en, pos_ru in zip(
                    ['noun',
                     'verb',
                     'adjective',
                     'adverb',
                     'pronoun',
                     'preposition',
                     'conjunction',
                     'interjection',
                     'determiner',
                     'article',
                     'particle',
                     'numeral',
                     'predicative'],

                    ['существительное',
                     'глагол',
                     'прилагательное',
                     'наречие',
                     'местоимение',
                     'предлог',
                     'союз',
                     'междометие',
                     'детерминатив',
                     'артикль',
                     'частица',
                     'числительное',
                     'предикатив'
                     ]
            ):
                conn.execute(
                    "INSERT OR IGNORE INTO parts_of_speech_const (pos_en, pos_ru) VALUES (?, ?)",
                    (pos_en, pos_ru, )
                             )
                conn.commit()

    def __create_table__translation_en_ru(self):
        """
        Таблица связей, содержит ссылки (id) на связанные слова  words_en и words_ru,
        тип части речи parts_of_speech_const,
        а так же численный показатель от 1 до 15, указывающий на частоту употребления в данном переводе.
        """

        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                '''
                CREATE TABLE IF NOT EXISTS translation_en_ru (
                    id_word_en INTEGER NOT NULL,
                    id_word_ru INTEGER NOT NULL,
                    id_pos INTEGER NOT NULL,
                    frequency INTEGER,
                    FOREIGN KEY (id_word_en) REFERENCES words_en(id),
                    FOREIGN KEY (id_word_ru) REFERENCES words_ru(id),
                    FOREIGN KEY (id_pos) REFERENCES parts_of_speech_const(id),
                    UNIQUE(id_word_en, id_word_ru, id_pos, frequency)
                )
                '''
            )
            conn.commit()

    def __create_tables(self):
        """
        Метод-обёртка, создаёт три таблицы, вызывается в инициализаторе класса
        """
        [self.__create_table__words(lang) for lang in ['en', 'ru']]
        self.__create_table__parts_of_speech_const()
        self.__create_table__translation_en_ru()

    #  END create main tables BLOCK
    ####
    #  START operations with main tables BLOCK

    def __get_parts_of_speech_const(self) -> dict:
        """
        Метод возвращает полное содержание таблицы parts_of_speech_const в виде dict
        с немного изменённой морфологией и названиями ключей.
        :return [{pos_en: {'id': id, 'ru': pos_ru}, {}, ...]
        """
        with sqlite3.connect(self.db_path) as conn:
            r = conn.execute('SELECT * FROM parts_of_speech_const').fetchall()
            if not r:
                raise Exception(f"Ошибка при получении значений таблицы {self.db_path}.parts_of_speech_const")
            result = {}
            for item in r:
                result[item[1]] = {'id': item[0], 'ru': item[2]}
            return result

    async def __add_new_row_to_table__words(self, word: str, lang: str) -> int:
        """
        Добавляет запись (если её нет), возвращает ID.
        word:
        :return: ID строки.
        """
        if lang not in ['en', 'ru']:
            raise ValueError("Argument <lang> is not valid. It must be in ['en', 'ru']")

        async with aiosqlite.connect(self.db_path) as conn:
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
                    raise Exception(f"Ошибка при получении id, таблицы words_{lang}, базы данных {self.db_path}")

    async def add_new_couple_to_table__translation_en_ru(self, word_en: str, word_ru: str, pos: str, freq: int):
        id_word_en = await self.__add_new_row_to_table__words(word_en, 'en')
        id_word_ru = await self.__add_new_row_to_table__words(word_ru, 'ru')
        try:
            id_pos = self.parts_of_speech_const[pos]['id']
        except KeyError:
            print(f'ключ {pos} не содержится в аттрибуте <parts_of_speech_const>')
            raise KeyError

        async with aiosqlite.connect(self.db_path) as db:
            # попробуем вставить новую запись. если идентичная строка уже есть - скипаем
            await db.execute(
                'INSERT OR IGNORE INTO translation_en_ru (id_word_en, id_word_ru, id_pos, frequency) VALUES (?, ?, ?, ?)',
                (id_word_en, id_word_ru, id_pos, freq,)
            )
            await db.commit()


