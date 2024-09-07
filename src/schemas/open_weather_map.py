from pydantic import BaseModel, Field


class OpenWeatherMapCoordinates(BaseModel):
    """
    Model which represents 'coord' field in OpenWeatherMap API response.
    """

    lon: float
    lat: float


class OpenWeatherMapWeather(BaseModel):
    """
    Model which represents 'weather' field in OpenWeatherMap API response.
    """

    id: int
    main: str
    description: str
    icon: str


class OpenWeatherMapMain(BaseModel):
    """
    Model which represents 'main' field in OpenWeatherMap API response.
    """

    temp: float
    feels_like: float
    temp_min: float
    temp_max: float
    pressure: int
    humidity: int


class OpenWeatherMapWind(BaseModel):
    """
    Model which represents 'wind' field in OpenWeatherMap API response.
    """

    speed: float
    deg: int


class OpeWeatherMapClouds(BaseModel):
    """
    Model which represents 'clouds' field in OpenWeatherMap API response.
    """

    all: int


class OpenWeatherMapSys(BaseModel):
    """
    Model which represents 'sys' field in OpenWeatherMap API response.
    """

    type: int
    id: int
    message: float | None = None
    country: str
    sunrise: int
    sunset: int


class OpenWeatherMapRain(BaseModel):
    """
    Model which represents 'rain' field in OpenWeatherMap API response.
    """

    one_h: int | str | float = Field(alias="1h")
    three_h: int | str | float = Field(alias="3h")


class OpenWeatherMapSnow(BaseModel):
    """
    Model which represents 'snow' field in OpenWeatherMap API response.
    """

    one_h: int | str | float = Field(alias="1h")
    three_h: int | str | float = Field(alias="3h")


class OpenWeatherMapResponse(BaseModel):
    """
    Model which represents full response from OpenWeatherMap API.
    """

    coord: OpenWeatherMapCoordinates
    weather: list[OpenWeatherMapWeather]
    base: str
    main: OpenWeatherMapMain
    visibility: int
    wind: OpenWeatherMapWind | None = None
    clouds: OpeWeatherMapClouds | None = None
    rain: OpenWeatherMapRain | None = None
    show: OpenWeatherMapSnow | None = None
    dt: int
    sys: OpenWeatherMapSys | None = None
    timezone: int
    id: int
    name: str
    cod: int
