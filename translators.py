import requests
import read_env



#pip install python-dotenv
def get_yandex_translations(word, lang="en-ru", api_url=read_env.YANDEX_API_URL, api_key= read_env.YANDEX_API_KEY):
    params = {"key": api_key, "lang": lang, "text": word}
    response = requests.get(api_url, params=params)
    if response.status_code != 200:
        return f"Error: {response.status_code}"
    data = response.json()
    print(data)
    if not data.get("def"):
        return None
    translations = []
    for item in data["def"]:
        for tr in item.get("tr", []):
            translations.append(tr["text"])
    return translations

# Пример использования
translations = get_yandex_translations("Love")
print(translations)