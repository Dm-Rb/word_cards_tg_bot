from config_file import config
import requests
from bot.globals import database

class YandexDictionaryRequests:
    api_url = config.YANDEX_API_URL
    api_key = config.YANDEX_API_KEY
    db_pos = database.parts_of_speech_const
    def make_request_to_api_syn(self, word: str, lang: str = "en-ru") -> list or None:
        if lang not in ["en-ru", "ru-en"]:
            raise ValueError('argument <lang> is not valid')
        params = {"key": self.api_key, "lang": lang, "text": word}
        response = requests.get(self.api_url, params=params)
        if response.status_code != 200:
            return f"Error: {response.status_code}"
        r_data = response.json()

        return r_data.get('def', None)

    @classmethod
    def parse_array(cls, r_data) -> list[dict]:
        # разбирает на массив словарей.
        # каждый словарь имеет вид {'word_en': str, 'word_ru': str, 'pos': str, 'freq': int
        result_array = []
        for item in r_data:
            for tr_item in item['tr']:
                elem = {
                    'word_en': item['text'],
                    'word_ru': tr_item['text'],
                    'pos_en': tr_item['pos'],
                    'pos_ru': cls.db_pos[tr_item['pos']]['ru'],
                    'freq': tr_item['fr']
                }
                result_array.append(elem)
        return result_array


#test
# from bot.globals import database
# #
# ya = YandexDictionaryRequests()
# data = ya.make_request_to_api_syn('should', 'en-ru')
# items = ya.parse_array(data)
# #
# async def d():
#     for item in items:
#         print(item)
#         await database.add_new_couple_to_table__translation_en_ru(item['word_en'], item['word_ru'], item['pos'], item['freq'])
#
#
#
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(d())


# from bot.globals import database
# #
#
# #
# async def d():
#     item = await database.get_translations_word_by_id(1, 'en')
#     print(item)
#
#
# if __name__ == "__main__":
#     import asyncio
#     asyncio.run(d())