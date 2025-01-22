from bot.globals import database
import pymorphy2
from bot.services.utils import grouping_array_by_pos, preparing_array_tuple2dict

class WordsTraining:

    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()

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
        unique_variants.remove(word)
        return unique_variants

    async def get_preparing_words_4_training(self, user_id):
        preparing_data = []

        user_data = await database.get_word_id_list_by_user_id__user_data(user_id)
        if not user_data:
            return

        for item in user_data:
            row = {'word_en_id': item[1], 'learning_level': item[2]}
            word_details = await database.get_array_of_transl_word_by_id(item[1])
            word_details = grouping_array_by_pos(preparing_array_tuple2dict(word_details))
            if not word_details:
                continue
            # Получаем лексемы для каждого варианта перевода
            try:
                for i in range(len(word_details['translation'])):
                    for j in range(len((word_details['translation'][i]['words_list']))):
                        lexemes = self.get_lexemes(word_details['translation'][i]['words_list'][j]['word'])
                        # Добавляем варианты лексем в массив
                        word_details['translation'][i]['words_list'][j]['lexemes'] = lexemes
                preparing_data.append(word_details)
            except TypeError:
                print(TypeError)
                continue

        return preparing_data

    def trainer_choice_word(self, word_en, word_ru, lexemes_ru, false_friends):
        pass

words_training = WordsTraining()
