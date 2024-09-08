import os
from moviepy.editor import VideoFileClip
from PIL import Image, ImageDraw, ImageFont, ImageSequence

from src.schemas import OpenWeatherMapResponse


class AvatarGenerator:
    """
    Class that generates avatar with current time and weather data
    (if it is available).
    """

    def __init__(
            self,
            font_file: str,
            image_folder: str,
            text_color: tuple[int] = (0, 0, 0),
            bg_color: tuple[int] = (255, 255, 255),
            bg_gif: str | None = None,
    ):
        """
        Initializer.
        Args:
            font_file: path to font file.
            image_folder: path to folder with weather icons.
            text_color: text color in RGB format.
            bg_color: background color in RGB format.
            bg_gif: path to background gif file.
        """

        self._text_color = text_color
        self._bg_color = bg_color
        self._folder = image_folder
        self._font_temperature = ImageFont.truetype(font_file, 30)
        self._font_min_max_temperature = ImageFont.truetype(font_file, 15)
        # Open base GIF is necessary
        self._bg_gif = Image.open(bg_gif) if bg_gif else None

    @staticmethod
    def _format_temperature(n: int | float) -> str:
        """ Adding sign and symbol 'C' around number. """

        n = int(n)
        result = u"{} C".format(str(n))
        if n >= 0:
            result = "+" + result
        return result

    def generate(
            self,
            weather_data: OpenWeatherMapResponse,
    ) -> os.path:
        """
        Method which generates avatar image with time and current weather data
        or only with current time if weather data is not available.
        Returns:
            os.path object - absolute path to the generated avatar image.
        """

        # Create background
        bg_color = self._bg_color + ((0,) if self._bg_gif else (255,))
        bg = Image.new(mode="RGBA", size=(200, 200), color=bg_color)
        canvas = ImageDraw.Draw(bg)
        # Prepare weather icon
        icon_path = os.path.join(
            self._folder,
            weather_data.weather[0].icon + ".png",
        )
        icon = Image.open(icon_path, "r")
        # Draw icon on background
        bg.paste(im=icon, box=(50, 15), mask=icon)
        # Draw temperature on background
        canvas.text(
            xy=(65, 100),
            text=self._format_temperature(weather_data.main.temp),
            font=self._font_temperature,
            fill=self._text_color,
        )
        # Draw humidity and wind speed info
        canvas.text(
            xy=(55, 130),
            text=f"{weather_data.main.humidity}%   {weather_data.wind.speed} m/c",
            font=self._font_min_max_temperature,
            fill=self._text_color,
        )
        if self._bg_gif:
            # Set gif if necessary
            result_file = "avatar.mp4"
            frames = []
            to_frame = bg.copy()
            for frame in ImageSequence.Iterator(self._bg_gif):
                new_frame = frame.copy()
                new_frame = new_frame.resize((200, 200))
                new_frame = new_frame.convert("RGBA")
                new_frame.alpha_composite(to_frame)
                frames.append(new_frame)
            frames[0].save(
                "avatar.gif",
                save_all=True,
                append_images=frames[1:-1],
            )
            # Convert to MP4
            clip = VideoFileClip("avatar.gif")
            clip.write_videofile(result_file, logger=None, audio=False)
        else:
            # Saving new avatar
            result_file = "avatar.png"
            bg.save(result_file)

        return os.path.abspath(result_file)


if __name__ == "__main__":

    data = {
        'coord': {'lon': 37.6156, 'lat': 55.7522},
        'weather': [{
            'id': 800,
            'main': 'Clear',
            'description': 'clear sky',
            'icon': '01d',
        }],
        'base': 'stations',
        'main': {'temp': 23.4, 'feels_like': 295.12, 'temp_min': 295.39, 'temp_max': 296.25, 'pressure': 1029, 'humidity': 46},
        'visibility': 10000,
        'wind': {'speed': 0.67, 'deg': 50},
        'clouds': {'all': 5},
        'rain': None,
        'show': None,
        'dt': 1725724090,
        'sys': {'type': 2, 'id': 2095214, 'message': None, 'country': 'RU', 'sunrise': 1725677189, 'sunset': 1725725334},
        'timezone': 10800,
        'id': 524901,
        'name': 'Moscow',
        'cod': 200,
    }

    ag = AvatarGenerator(
        font_file="../data/OpenSans-Regular.ttf",
        image_folder="../../temp",
        bg_gif="../data/bg_gif.gif",
        text_color=(255,255,255),
    )
    path = ag.generate(weather_data=OpenWeatherMapResponse(**data))
    print(path)