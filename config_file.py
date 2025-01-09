import os
from dotenv import load_dotenv

# загружаем переменные окружения из .env
load_dotenv()

class Config:
    BOT_TOKEN = os.getenv("BOT_TOKEN")
    YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
    YANDEX_API_URL = os.getenv("YANDEX_API_URL")

# екземпляр конфигурации для импорта и использования
config = Config()
