from config_file import config
import requests
from bot.globals import database
import aiohttp


class YandexDictionaryApi:

    api_url = config.YANDEX_API_URL
    api_key = config.YANDEX_API_KEY
    db_pos = database.parts_of_speech_const

    async def fetch_data(self, word, lang):
        lang_dict = {'en': 'en-ru', 'ru': 'ru-en'}
        params = {"key": self.api_key, "lang": lang_dict[lang], "text": word}
        async with aiohttp.ClientSession() as session:
            async with session.get(url=self.api_url, params=params) as response:
                if response.status != 200:
                    return None
                return await response.json()

    def parse_array(self, r_data, lang) -> list[dict]:
        # разбирает на массив словарей.
        # каждый словарь имеет вид {'word_en': str, 'word_ru': str, 'pos': str, 'freq': int
        result_array = []
        for item in r_data['def']:
            for tr_item in item['tr']:
                elem = {
                    'word_en': item['text'] if lang == 'en' else tr_item['text'],
                    'word_ru': tr_item['text'] if lang == 'en' else item['text'],
                    'pos_en': tr_item['pos'],
                    'pos_ru': self.db_pos[tr_item['pos']]['ru'],
                    'freq': tr_item['fr']
                }
                result_array.append(elem)
        return result_array

    def fetch_data_sync(self, word: str, lang: str) -> list or None:
        if lang not in ["en-ru", "ru-en"]:
            raise ValueError('argument <lang> is not valid')
        params = {"key": self.api_key, "lang": lang, "text": word}
        response = requests.get(self.api_url, params=params)
        if response.status_code != 200:
            return f"Error: {response.status_code}"
        r_data = response.json()

        return r_data

    async def get_word_details_from_ya_dict(self, word, lang):
        # Проверяет валидность аргумента <lang>
        if lang not in ['en', 'ru']:
            raise ValueError("Argument <lang> is not valid. It must be in ['en', 'ru']")
        response = await self.fetch_data(word, lang)
        if not response:
            return
        return self.parse_array(response, lang)


#  инициализация объекта для импорта
ya_dict_api = YandexDictionaryApi()
