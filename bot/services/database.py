import aiosqlite
import sqlite3
from os.path import join as join_path


class DataBase:

    def __init__(self, db_name: str = 'dictionary_userdata.db', db_path='files'):
        self.db_path = join_path(db_path, db_name)
        # create tables if it not exist
        self.__create_tables()
        # vars
        self.parts_of_speech_const = self.__get_parts_of_speech_const()  # [{pos_en: {'id': id, 'ru': pos_ru}, {}, ...]

    #  ### START create tables BLOCK ###

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

    def __create_table__user_dicts(self):
        """
        Таблица для пользовательских словарей
        """
        with sqlite3.connect(self.db_path) as conn:
            conn.execute(
                f'''
                CREATE TABLE IF NOT EXISTS user_data (
                    id_tg_user TEXT NOT NULL,
                    id_word_en INTEGER NOT NULL,
                    learning_level INTEGER DEFAULT 0,
                    last_review_datetime TEXT NOT NULL CHECK (LENGTH(last_review_datetime) = 19),
                    next_review_datetime TEXT CHECK (LENGTH(next_review_datetime) = 19),
                    FOREIGN KEY (id_word_en) REFERENCES words_en(id)
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
        self.__create_table__user_dicts()

    #  ### END create tables BLOCK ###

    ###

    #  ### START operations with tables of main dictionary (en/ru words and their relationships) BLOCK ###

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

    async def __add_new_row_to_table__words(self, word: str, lang: str):
        """
        !Eсли слова (word) нет в тбл.(words_{lang}):
            добавляет слово (word) в указанную (lang) таблицу и возвращает ID новой записи
        !Если слово (word) присутствует в тбл.(words_{lang}):
            возвращает его ID
        :param word: str - слово (en или ru)
        :param lang: str - тип таблицы БД со словами, к которой нужно обратиться (en или ru)
        :return int - возвращает id слова

        """
        # Проверяет валидность аргумента <lang>
        if lang not in ['en', 'ru']:
            raise ValueError("Argument <lang> is not valid. It must be in ['en', 'ru']")
        # ---
        async with aiosqlite.connect(self.db_path) as conn:
            # Попробует вставить новую запись. Если идентичная строка уже есть (парам. UNIQUE) - скипает
            await conn.execute(
                f'INSERT OR IGNORE INTO words_{lang} (word) VALUES (?)',
                (word, )
            )
            await conn.commit()
            # на ст.ов.фл рекомендуют закрывать коннектор, но я хуй знает зачем, ведь тут менеджер контекста
            await conn.close()

        # Получает ID строки
        await self.get_row_id_by_value_from_table__words(word, lang)

    async def get_row_id_by_value_from_table__words(self, word: str, lang: str) -> int or False:
        """
        Проверяет наличие слова в таблице указанного типа.
        Если слово есть - возвращает его табличый ID, нет - False
        :param word: str - слово (en или ru)
        :param lang: str - тип таблицы БД со словами, к которой нужно обратиться (en или ru)
        :return: int or False - возвращает id слова или False
        """
        # Проверяет валидность аргумента <lang>
        if lang not in ['en', 'ru']:
            raise ValueError("Argument <lang> is not valid. It must be in ['en', 'ru']")
        # ---
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.execute(f'SELECT id FROM words_{lang} WHERE word = ?', (word,))
            row = await cursor.fetchone()
            if row:
                return row[0]
            else:
                return False

    async def add_new_couple_to_table__translation_en_ru(self, word_en: str, word_ru: str, pos: str, freq: int):
        """
        Добавляет новую строку в таблицу translation_en_ru.
        Данная таблица - основной словарь, где лежит слово/перевод/часть речи/частота употребления в данном переводе
        :param word_en: str - слово en
        :param word_ru: str - слово ru
        :param pos: str - (part of speech) наазвание части речи на en
        :param freq: int - число, указывающее на частоту употребления слова в данном переводе
        """
        # Получает табличные id слов (ищет существующие слова или добавляет в таблицу в случае отсутствия)
        id_word_en = await self.__add_new_row_to_table__words(word_en, 'en')
        id_word_ru = await self.__add_new_row_to_table__words(word_ru, 'ru')
        # Получает табличные id части речи по его имени из атрибута объекта (типа кеш)
        try:
            id_pos = self.parts_of_speech_const[pos]['id']
        except KeyError:
            print(f'ключ {pos} не содержится в аттрибуте <parts_of_speech_const>')
            raise KeyError

        async with aiosqlite.connect(self.db_path) as db:
            # Попробует вставить новую запись. Если идентичная строка уже есть (парам. UNIQUE) - скипает
            await db.execute(
                'INSERT OR IGNORE INTO translation_en_ru (id_word_en, id_word_ru, id_pos, frequency) VALUES (?, ?, ?, ?)',
                (id_word_en, id_word_ru, id_pos, freq,)
            )
            await db.commit()

    async def get_translations_word_by_id(self, word_id: int, lang: str = 'en'):
        """
        Извлекает все связанные с английским словом переводы и всю сопутствующую информацию (часть речи, частота употр.)
        Возвращает список кортежей по схеме: [('en_word', 'ru_word', 'pos_en', 'pos_ru', frequency)]
        Например:
        [
            ('should', 'должны', 'adjective', 'прилагательное', 10),
            ('should', 'необходимо', 'predicative', 'предикатив', 5)
        ]
        :param word_id: int - табличный id слова en_word или ru_word
        :param lang: str - тип таблицы (ru или en). Иными словами это указатель на то, на каком языке передаётся word_id
        :return:
        """
        # Меняет число en_word_id с type(str) на type(unt) если вдруг по какой то причине данный аргумент прилетел в str
        if isinstance(word_id, str) and word_id.isdigit():
            word_id = int(word_id)
        # ---
        # Проверяет валидность аргумента <lang>
        if lang not in ['en', 'ru']:
            raise ValueError(f'Переданый в функцию аргумент lang={lang} не валиден')
        # ---
        async with aiosqlite.connect(self.db_path) as conn:
            cursor = await conn.cursor()
            await cursor.execute(
                f"""
                SELECT 
                    words_en.word AS word_en,
                    words_ru.word AS word_ru,
                    parts_of_speech_const.pos_en AS pos_en,
                    parts_of_speech_const.pos_ru AS pos_ru,
                    translation_en_ru.frequency
                FROM translation_en_ru
                JOIN words_en ON translation_en_ru.id_word_en = words_en.id
                JOIN words_ru ON translation_en_ru.id_word_ru = words_ru.id
                JOIN parts_of_speech_const ON translation_en_ru.id_pos = parts_of_speech_const.id
                WHERE translation_en_ru.id_word_{lang} = ?;
                """, (word_id,)
            )
            result = await cursor.fetchall()  # Получаем все строки результата асинхронно
            await cursor.close()

        return result

    # ### END operations with tables of main dictionary (en/ru words and their relationships) BLOCK ###
