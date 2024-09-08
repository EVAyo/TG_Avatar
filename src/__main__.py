from aiohttp import ClientSession
from asyncio import Future
from socks import SOCKS5
from telethon import TelegramClient
from uvloop import run

from src.application import Application
from src.config import ApplicationConfig
from src.schemas import ApplicationContext
from src.services import AvatarGenerator, OpenWeatherMapAPI
from src.utils import CustomJSONLogger


async def create_context() -> ApplicationContext:
    # Creating an instance of TelegramClient class
    if not all((
            ApplicationConfig.PROXY_IP,
            ApplicationConfig.PROXY_PORT,
            ApplicationConfig.PROXY_PASS,
    )):
        proxy = None
    else:
        proxy = (
            SOCKS5,
            ApplicationConfig.PROXY_IP,
            ApplicationConfig.PROXY_PORT,
            True,
            ApplicationConfig.PROXY_PASS,
            ApplicationConfig.PROXY_PASS,
        )
    client = TelegramClient(
        'TG_Avatar',  # Session name
        api_id=ApplicationConfig.TELEGRAM_API_ID,      # Telegram API ID
        api_hash=ApplicationConfig.TELEGRAM_API_HASH,  # Telegram API hash
        proxy=proxy,                                   # Proxy data
    )
    # Create Logger
    logger = CustomJSONLogger(name="tg_avatar")
    # Create avatar generator instance
    avatar_generator = AvatarGenerator(
        font_file=ApplicationConfig.FONT_FILE_NAME,
        image_folder=ApplicationConfig.WEATHER_ICONS_FOLDER_NAME,
        text_color=ApplicationConfig.TEXT_COLOR,
        bg_color=ApplicationConfig.BACKGROUND_COLOR,
        bg_gif=ApplicationConfig.BG_GIF_PATH,
    )
    # Create service for OpenWeatherMap API calls
    open_weather_map = OpenWeatherMapAPI(
        api_token=ApplicationConfig.OPENWEATHER_API_KEY,
        api_url=ApplicationConfig.OPENWEATHER_API_URL,
        image_url_template=ApplicationConfig.OPENWEATHER_API_IMAGE_URL,
        cache_folder_path=ApplicationConfig.WEATHER_ICONS_FOLDER_NAME,
        city_id=ApplicationConfig.OPENWEATHER_API_CITYID,
        logger=logger,
        client_session=ClientSession(),
    )
    return ApplicationContext(
        avatar_generator=avatar_generator,
        open_weather_map=open_weather_map,
        tg_client=client,
        config=ApplicationConfig,
        logger=logger,
    )


async def main():
    context = await create_context()
    application = Application(context)
    try:
        await application.setup()
        await Future()
    finally:
        application.teardown()


if __name__ == "__main__":

    run(main())
