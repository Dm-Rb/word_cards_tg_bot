import os
from dotenv import load_dotenv


load_dotenv()
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
YANDEX_API_URL = os.getenv("YANDEX_API_URL")