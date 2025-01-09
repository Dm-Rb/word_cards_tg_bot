from config_file import config
import requests
import re
from bot.services.database import DataBaseDictionary


class YandexDictionaryRequests:
    api_url = config.YANDEX_API_URL
    api_key = config.YANDEX_API_KEY

    def make_request_to_api_syn(self, word: str, lang: str = "en-ru") -> list or None:
        if lang not in ["en-ru", "ru-en"]:
            raise ValueError('argument <lang> is not valid')
        params = {"key": self.api_key, "lang": lang, "text": word}
        response = requests.get(self.api_url, params=params)
        if response.status_code != 200:
            return f"Error: {response.status_code}"
        r_data = response.json()

        return r_data.get('def', None)

    @staticmethod
    def parse_array(r_data) -> list[dict]:
        # разбирает на массив словарей.
        # каждый словарь имеет вид {'word_en': str, 'word_ru': str, 'pos': str, 'freq': int
        result_array = []
        for item in r_data:
            for tr_item in item['tr']:
                elem = {
                    'word_en': item['text'],
                    'word_ru': tr_item['text'],
                    'pos': tr_item['pos'],
                    'freq': tr_item['fr']
                }
                result_array.append(elem)
        return result_array

    @staticmethod
    def detect_language(word):
        # проверка на английские литеры
        if re.fullmatch(r'[A-Za-z]+', word):
            return 'en-ru'
        # проверка на русские литеры
        elif re.fullmatch(r'[А-Яа-яЁё]+', word):
            return 'ru-en'
        else:
            # смешанные символы или не только буквы
            return None

# test
ya = YandexDictionaryRequests()
data = ya.make_request_to_api_syn('should', 'en-ru')
r = ya.parse_array(data)
db = DataBaseDictionary()
async def d():
    for item in r:
        await db.add_new_couple_to_table__translation_en_ru(*item.values())
        print(item)

if __name__ == "__main__":
    import asyncio
    asyncio.run(d())