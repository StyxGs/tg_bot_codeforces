import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()

TOKEN: str = os.environ.get('TOKEN')

DB_USER: str = os.environ.get('DB_USER')
DB_PASS: str = os.environ.get('DB_PASS')
DB_HOST: str = os.environ.get('DB_HOST')
DB_PORT: str = os.environ.get('DB_PORT')
DB_NAME: str = os.environ.get('DB_NAME')
REDIS_PORT: int = os.environ.get('REDIS_PORT')
REDIS_HOST: str = os.environ.get('REDIS_HOST')


@dataclass
class TgBot:
    token: str


def load_config(path: str | None = None) -> TgBot:
    """Функция для загрузки конфигурационных данных о боте"""
    return TgBot(token=TOKEN)
