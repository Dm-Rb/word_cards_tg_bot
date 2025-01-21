# from bot.globals import database
import pymorphy2


class WordsTraining:

    # таблица соответствий констант из pymorphy2
    soe_db_pymorphy2 = {
        'noun': 'NOUN',
        'adjective': 'ADJF',
        'participle': 'PRTF',
        'adverb': 'ADVB',
        'pronoun': 'NPRO',
        'preposition': 'PREP',
        'conjunction': 'CONJ',
        'interjection': 'INTJ',
        'determiner': '',
        'particle': 'PRCL',
        'numeral': 'NUMR',
        'predicative': 'PRED'
    }
