# from bot.globals import database
import pymorphy2


class WordsTraining:

    # таблица соответствий констант из pymorphy2
    pos_db_pymorphy2 = {
        'noun': 'NOUN',
        'adjective': 'ADJF',
        'participle': 'PRTF',
        'adverb': 'ADVB',
        'pronoun': 'NPRO',
        'preposition': 'PREP',
        'conjunction': 'CONJ',
        'interjection': 'INTJ',
        'particle': 'PRCL',
        'numeral': 'NUMR',
        'predicative': 'PRED'
    }

    def __init__(self):
        self.morph = pymorphy2.MorphAnalyzer()
    def get_morphological_analogues_ru(self, word_ru, pos):
        parsed_word = self.morph.parse(word_ru)[0]  # Берем первую интерпретацию

        forms = {form.word for form in parsed_word.lexeme if form.tag.POS == pos}
        return forms
d = WordsTraining()
r = d.get_morphological_analogues_ru('замок', 'NOUN')
print(r)