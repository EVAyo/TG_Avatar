import os
from asyncio import sleep as aio_sleep, Task, create_task
from telethon.tl.functions.photos import (
    UploadProfilePhotoRequest, DeletePhotosRequest
)
from traceback import format_exception
from sys import exc_info

from src.config import ApplicationConfig
from src.exceptions import OpenWeatherMapAPIError
from src.schemas import ApplicationContext


class Application:

    def __init__(self,context: ApplicationContext):
        self.context = context
        self.task: Task | None = None

    async def main_task(self):
        while True:
            try:
                # Request weather data (icon loads inside)
                weather = await self.context.open_weather_map.get_weather_data()
                # Generate and upload new avatar
                new_file_path = self.context.avatar_generator.generate(weather)
                new = await self.context.tg_client.upload_file(new_file_path)
                # Deleting Telegram avatar
                current = await self.context.tg_client.get_profile_photos("me")
                await self.context.tg_client(DeletePhotosRequest(current))
                # Updating Telegram avatar
                key = "video" if self.context.config.BG_GIF_PATH else "file"
                await self.context.tg_client(UploadProfilePhotoRequest(**{key: new}))
            except OpenWeatherMapAPIError as e:
                self.context.logger.error({
                    "event": "error",
                    "error": str(e),
                    "traceback": format_exception(*exc_info()),
                })
                await aio_sleep(60)
            else:
                await aio_sleep(600)

    async def setup(self):
        self.context.logger.info({"event": "startup"})
        # Create folder for weather images if not exists
        if not os.path.exists(ApplicationConfig.WEATHER_ICONS_FOLDER_NAME):
            os.mkdir(ApplicationConfig.WEATHER_ICONS_FOLDER_NAME)
        # Start Telethon client
        await self.context.tg_client.start(
            phone=lambda: self.context.config.TELEGRAM_PHONE,
            password=lambda: self.context.config.TELEGRAM_PASSWORD,
        )
        # Start background task
        self.task = create_task(self.main_task())
        self.context.logger.info({"event": "startup complete"})

    def teardown(self):
        self.context.logger.info({"event": "teardown"})
        if self.task is not None:
            self.task.cancel()
        self.context.logger.info({"event": "teardown complete"})
