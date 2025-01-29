from bot.globals import database
import pymorphy2
from bot.services.utils import grouping_array_by_pos, preparing_array_tuple2dict
from bot.templates.text import question_without_context, show_statistic_training
from bot.keyboards.reply import kb_with_answer_options
from random import choice, sample, shuffle

class WordsTraining:

    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()
        self.users_data = {}
        self.users_training_statistics = {}

    def get_lexemes(self, word: str) -> list:
        # Получаем все возможные разборы слова
        parsed_word = self.morph.parse(word)

        # Если разборов нет, возвращаем пустой список
        if not parsed_word:
            return []

        # Определяем часть речи и число первого разбора (обычно это наиболее вероятный вариант)
        part_of_speech = parsed_word[0].tag.POS  # Часть речи
        number = parsed_word[0].tag.number  # Число (единственное или множественное)

        # Список для хранения результатов
        variants = []

        # Перебираем все возможные разборы
        for parse in parsed_word:
            # Проверяем, соответствует ли часть речи и число определенным
            if parse.tag.POS == part_of_speech and parse.tag.number == number:
                # Получаем все формы слова (лексемы) для этой части речи
                lexemes = parse.lexeme
                # Фильтруем формы, оставляя только те, которые соответствуют исходной части речи и числу
                for lexeme in lexemes:
                    if lexeme.tag.POS == part_of_speech and lexeme.tag.number == number:
                        variants.append(lexeme.word)

        # Убираем дубликаты, если они есть
        unique_variants = list(set(variants))
        # Удаляем из списка базовое слово
        try:
            unique_variants.remove(word)
        except ValueError:
            pass
        return unique_variants

    async def create_array_with_user_data(self, user_id):
        preparing_data = []

        user_data = await database.get_word_id_list_by_user_id__user_data(user_id)
        if not user_data:
            return

        for item in user_data:
            word_details = await database.get_array_of_transl_word_by_id(item[1])
            word_details = grouping_array_by_pos(preparing_array_tuple2dict(word_details))
            if not word_details:
                continue
            # Получаем лексемы для каждого варианта перевода
            try:
                for i in range(len(word_details['translations'])):
                    for j in range(len((word_details['translations'][i]['words_list']))):
                        lexemes = self.get_lexemes(word_details['translations'][i]['words_list'][j]['word'])
                        # Добавляем варианты лексем в массив
                        word_details['translations'][i]['words_list'][j]['lexemes'] = lexemes

                # Добавляем информацию из <item>
                word_details['word_en_id'] = item[1]
                word_details['learning_level'] = item[2]
                word_details['random_words_ru'] = await database.get_random_wrong_answers(word_details['word'])
                preparing_data.append(word_details)
            except TypeError:
                print(TypeError)
                continue
        #preparing_data = [{'word': 'run', 'lang': 'en', 'translations': [{'pos_en': 'verb', 'pos_ru': 'глагол', 'words_list': [{'word': 'бежать', 'freq': 10, 'lexemes': []}, {'word': 'работать', 'freq': 10, 'lexemes': []}, {'word': 'запустить', 'freq': 10, 'lexemes': []}, {'word': 'проходить', 'freq': 5, 'lexemes': []}, {'word': 'управлять', 'freq': 5, 'lexemes': []}, {'word': 'выполнить', 'freq': 5, 'lexemes': []}, {'word': 'убежать', 'freq': 5, 'lexemes': []}, {'word': 'баллотироваться', 'freq': 1, 'lexemes': []}]}, {'pos_en': 'noun', 'pos_ru': 'существительное', 'words_list': [{'word': 'бег', 'freq': 5, 'lexemes': ['беге', 'бега', 'бегом', 'бегу']}, {'word': 'запуск', 'freq': 5, 'lexemes': ['запуску', 'запуска', 'запуском', 'запуске']}, {'word': 'выполнение', 'freq': 5, 'lexemes': ['выполненью', 'выполненье', 'выполненья', 'выполнении', 'выполнением', 'выполненьем', 'выполнения', 'выполненьи', 'выполнению']}, {'word': 'пробег', 'freq': 1, 'lexemes': ['пробега', 'пробегом', 'пробегу', 'пробеге']}]}]}, {'word': 'sleep', 'lang': 'en', 'translation': [{'pos_en': 'noun', 'pos_ru': 'существительное', 'words_list': [{'word': 'сон', 'freq': 10, 'lexemes': ['сна', 'сном', 'сне', 'сну']}, {'word': 'режим сна', 'freq': 1, 'lexemes': ['режим сон', 'режим сной', 'режим сне', 'режим сном', 'режим сною', 'режим сны', 'режим сну']}, {'word': 'ночлег', 'freq': 1, 'lexemes': ['ночлега', 'ночлегу', 'ночлеге', 'ночлегом']}, {'word': 'спячка', 'freq': 1, 'lexemes': ['спячкой', 'спячку', 'спячки', 'спячке', 'спячкою']}]}, {'pos_en': 'verb', 'pos_ru': 'глагол', 'words_list': [{'word': 'ночевать', 'freq': 5, 'lexemes': []}, {'word': 'засыпать', 'freq': 5, 'lexemes': []}, {'word': 'поспать', 'freq': 5, 'lexemes': []}, {'word': 'дремать', 'freq': 1, 'lexemes': []}, {'word': 'спаться', 'freq': 1, 'lexemes': []}, {'word': 'отсыпаться', 'freq': 1, 'lexemes': []}, {'word': 'усыплять', 'freq': 1, 'lexemes': []}]}, {'pos_en': 'adjective', 'pos_ru': 'прилагательное', 'words_list': [{'word': 'сонный', 'freq': 1, 'lexemes': ['сонное', 'сонном', 'сонному', 'сонную', 'сонною', 'сонной', 'сонным', 'сонная', 'сонного']}]}]}]
        return preparing_data

    def get_question_without_context(self, user_id, i_array, i_subarray, clue=False):
        word = self.users_data[user_id][i_array]['word']
        pos_en = self.users_data[user_id][i_array]['translations'][i_subarray]['pos_en']
        pos_ru = self.users_data[user_id][i_array]['translations'][i_subarray]['pos_ru']
        if clue:
            # Выбрать рандомный перевод для слова из списка переводов
            random_translation_ru = choice(self.users_data[user_id][i_array]['translations'][i_subarray]['words_list'])
            random_translation_ru = random_translation_ru.get('word', None)
        else:
            random_translation_ru = None
        return question_without_context(word, pos_en, pos_ru, random_translation_ru)

    def generate_keyboard(self, user_id, i_array, i_subarray):
        # Выбрать рандомный перевод для слова из списка переводов
        random_translation_ru = choice(self.users_data[user_id][i_array]['translations'][i_subarray]['words_list'])
        random_translation_ru = random_translation_ru.get('word', None)
        # Выбрать 3 рандомные слова ru СТРОГО ИСКЛЮЧАЯ слова являющиеся переводами для word_en
        random_words_ru = sample(self.users_data[user_id][i_array]['random_words_ru'], 3)

        random_words_ru.append(random_translation_ru)
        shuffle(random_words_ru)
        return kb_with_answer_options(random_words_ru)

    def check_answer_without_context(self, answer: str, user_id: str, i_array: int, i_subarray: int):
        """
        Эта функция проверяет перевод слова без контекста. Т.е для слова создаётся массив со всеми возможными переводами,
        которые соответствуют части речи для этого слова.
        """
        word = self.users_data[user_id][i_array]['word']
        translations = self.users_data[user_id][i_array]['translations'][i_subarray]
        words = []
        lexemes = []
        for item in translations['words_list']:
            words.append(item['word'].lower())
            if item['lexemes']:
                lexemes.extend(item.lower() for item in item['lexemes'])

        is_correct = answer.lower() in words or answer.lower() in lexemes
        statistic_item = {
            'word': word,
            "pos": translations["pos_en"],
            'user_answer': answer,
            "answer_is_correct": is_correct,
            "correct_words": words

        }
        if not self.users_training_statistics.get(user_id, None):
            # self.users_training_statistics[user_id]['start_datetime'] = datetime.datetime.now()
            self.users_training_statistics[user_id] = [statistic_item]
        else:
            self.users_training_statistics[user_id].append(statistic_item)

    def show_training_result(self, user_id):
        return show_statistic_training(self.users_training_statistics[user_id])

    async def get_user_data_array(self, user_id):
        """
        Функция-обёртка для запроса пользовательских данных (слова, добавленные для тренировки)
        :param user_id:
        :return:
        """
        if not self.users_data.get(user_id, None):
            users_data = await self.create_array_with_user_data(user_id)
            self.users_data[user_id] = users_data
        return self.users_data[user_id]


words_training = WordsTraining()
