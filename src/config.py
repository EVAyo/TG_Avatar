from dataclasses import dataclass
from os import environ


@dataclass
class ApplicationConfig:

    # A folder name where weather icons will be collecting.
    WEATHER_ICONS_FOLDER_NAME = environ.get("WEATHER_ICONS_FOLDER_NAME", "cache")

    # Telegram API constants
    TELEGRAM_API_ID:    int = int(environ.get("TG_AVATAR_TELEGRAM_API_ID", "0"))
    TELEGRAM_API_HASH:  str = environ.get("TG_AVATAR_TELEGRAM_API_HASH", "")
    TELEGRAM_PHONE:     str = environ.get("TG_AVATAR_TELEGRAM_PHONE", "")
    TELEGRAM_PASSWORD:  str = environ.get("TG_AVATAR_TELEGRAM_PASSWORD", "")

    # Proxy data (keep it empty if not necessary)
    PROXY_IP:    str = environ.get("TG_AVATAR_PROXY_IP", "")
    PROXY_PORT:  int = int(environ.get("TG_AVATAR_PROXY_PORT", "") or "0")
    PROXY_PASS:  str = environ.get("TG_AVATAR_PROXY_PASSWORD", "")

    # OpenWeather API
    OPENWEATHER_API_KEY:       str = environ.get("TG_AVATAR_OPENWEATHER_API_KEY", "")
    OPENWEATHER_API_URL:       str = environ.get("TG_AVATAR_OPENWEATHER_API_URL", "http://api.openweathermap.org/data/2.5/weather")
    OPENWEATHER_API_CITYID:    int = int(environ.get("TG_AVATAR_OPENWEATHER_API_CITY_ID", "524901"))
    OPENWEATHER_API_IMAGE_URL: str = environ.get("TG_AVATAR_OPENWEATHER_API_IMAGE_URL", "http://openweathermap.org/img/wn/{}@2x.png")

    # Customization
    BACKGROUND_COLOR: tuple[int] = tuple([
        int(n)
        for n in environ.get("TG_AVATAR_COLOR_BACKGROUND", "255,255,255").split(',')
    ])
    TEXT_COLOR: tuple[int] = tuple([
        int(n)
        for n in environ.get("TG_AVATAR_COLOR_TEXT", "255,255,255").split(',')
    ])
    FONT_FILE_NAME = environ.get("FONT_FILE_NAME", "src/data/OpenSans-Regular.ttf")
    BG_GIF_PATH = environ.get("BG_GIF_PATH", "src/data/bg_gif.gif")
