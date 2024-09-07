from dataclasses import dataclass
from telethon import TelegramClient
from typing import Type

from src.config import ApplicationConfig
from src.utils import CustomJSONLogger


@dataclass
class ApplicationContext:

    avatar_generator: "AvatarGenerator"
    open_weather_map: "OpenWeatherMapAPI"
    tg_client: TelegramClient
    config: Type[ApplicationConfig]
    logger: CustomJSONLogger
