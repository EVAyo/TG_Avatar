import os
from aiohttp import ClientSession, ClientOSError
from asyncio import sleep as aio_sleep
from pydantic import ValidationError
from sys import exc_info
from traceback import format_exception

from src.schemas import OpenWeatherMapResponse
from src.exceptions import WeatherDataDownloadError, ImageDownloadError
from src.utils import CustomJSONLogger


class OpenWeatherMapAPI:

    def __init__(
            self,
            api_token: str,
            api_url: str,
            image_url_template: str,
            cache_folder_path: str,
            city_id: str,
            logger: CustomJSONLogger,
            client_session: ClientSession,
    ):
        """
        Initializer.
        Args:
            api_token: OpenWeatherMap API token.
            api_url: OpenWeatherMap API URL.
            image_url_template: URL template for downloading weather image.
            cache_folder_path: path to folder where icons will be stored.
            logger: logger object.
            client_session: persistent client session.
        """

        self._api_token = api_token
        self._api_url = api_url
        self._api_image_url = image_url_template
        self._cache_folder_path = cache_folder_path
        self._city_id = city_id
        self._logger = logger
        self._client_session = client_session

    def _weather_image_exists(self, image_name: str) -> bool:
        """
        Check if weather image icon is exists in folder.
        Args:
            image_name: name of image (w/o extension).
        Returns:
            True if image is exist, else False.
        """

        img_path = os.path.join(self._cache_folder_path, image_name + ".png")
        exists = os.path.exists(img_path)
        self._logger.info({
            "event": "check_local_image",
            "image_name": image_name,
            "image_path": img_path,
            "is_exists": exists,
        })
        return exists

    async def get_weather_image(self, image_name: str) -> str:
        """
        Method which downloads a weather icon from OpenWeatherMap API.
        Args:
            image_name: name of weather icon (w/o extension).
        Raises:
            ImageDownloadError: if OpenWeatherMap API returns response
                with status code different from 200 or request raises
                aiohttp.ClientError.
        Returns:
            Path to new image.
        """

        url = self._api_image_url.format(image_name)
        self._logger.info({
            "event": "download_image",
            "image_name": image_name,
        })
        try:
            resp = await self._client_session.get(url=url)
        except (ConnectionResetError, ClientOSError) as e:
            self._logger.exception({
                "event": "error",
                "error": str(e),
                "traceback": format_exception(*exc_info()),
            })
            raise ImageDownloadError("Can't get image")
        if resp.status != 200:
            raise ImageDownloadError(f"Response status: {resp.status}")
        data = await resp.read()
        new_image_path = os.path.join(self._cache_folder_path, image_name + ".png")
        with open(new_image_path, "wb") as image_file:
            image_file.write(data)
        self._logger.info({
            "event": "load_complete",
            "image_name": image_name,
        })
        return new_image_path

    async def get_weather_data(self) -> OpenWeatherMapResponse | None:
        """
        Method which makes a GET request to OpenWeatherMap API in order to
        get current temperature and weather icon name to your city.
        Returns the tuple of updated weather data (temperature
        and weather icon name).
        Raises:
            WeatherDataDownloadError: if OpenWeatherMap API returns
                response with status code different from 200.
        Returns:
            tuple with current weather icon name and all weather data from API.
        """

        # Necessary information for request which loading in query string
        payload = {
            "id": self._city_id,
            "appid": self._api_token,
            "units": "metric",
        }
        self._logger.info({
            "event": "request_weather",
            "payload": payload,
            "url": self._api_url,
        })
        # Trying making request
        attempts = 3
        sleep_time = 5
        validated_response_body = None
        for i in range(attempts):
            try:
                response = await self._client_session.get(
                    url=self._api_url,
                    params=payload,
                )
                response_body = await response.json(encoding="utf-8")
                validated_response_body = OpenWeatherMapResponse(**response_body)
                self._logger.info({
                    "event": "response",
                    "data": validated_response_body.dict(),
                })
                icon_name = validated_response_body.weather[0].icon
                if not self._weather_image_exists(icon_name):
                    await self.get_weather_image(icon_name)
                break
            except (ConnectionResetError, ClientOSError, ValidationError) as request_error:
                self._logger.exception({
                    "event": "exception",
                    "error": str(request_error),
                    "traceback": format_exception(*exc_info()),
                })
                if i < attempts:
                    await aio_sleep(sleep_time)
                    continue
                raise WeatherDataDownloadError(
                    "Couldn't update weather data from OpenWeatherMap..."
                )
        return validated_response_body


if __name__ == "__main__":

    from uvloop import run

    async def test():
        sess = ClientSession()
        client = OpenWeatherMapAPI(
            api_token="3acafd9d9a74ab54bf6795da17256abf",
            api_url="http://api.openweathermap.org/data/2.5/weather",
            image_url_template="http://openweathermap.org/img/wn/{}@2x.png",
            city_id="524901",
            cache_folder_path="../../temp",
            logger=CustomJSONLogger(name="temp"),
            client_session=sess,
        )
        await client.get_weather_data()
        await sess.close()

    run(test())
