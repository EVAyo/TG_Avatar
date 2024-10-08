# TG_Avatar #

## Description ##

This script updates you avatar in Telegram every ten minutes with adding  
weather data (weather icon, temperature, humidity and wind speed) on it 
using Telegram API. Weather data getting from OpenWeatherMap API and 
updates every 10 minutes. If all works fine, you will see something like that:

![Avatar Example](examples/example_static.png)

You can also add background GIF for animating avatar 
(see "Customization"):

![Avatar Example Animated](examples/example_animated.gif)

## Getting Started ##

Before launching the script you should do some steps.

1. Telegram API

Get you own Telegram app api_id and app api_hash by following 
[this](https://core.telegram.org/api/obtaining_api_id) instruction.
Write them to `config.py` file or `.env` (in corresponds default values) with 
you phone number and password by adding corresponding values to variables.

2. OpenWeatherMap API

Get you own OpenWeatherMap API key from [there](https://openweathermap.org/api).
Note that you should create an account first. Write it to the 
`openweather_api_key` variable in `config.py` or `.env`. Then found you're 
city's id at openweathermap.org and write it to the 
`openweather_api_cityid` variable.

## Customization ##

### Colors

You can set text and background color by changing corresponds values 
in `config.py` file in block "customization" in manual launching mode or 
in `.env` file if launching in Docker.  
Note that values must be tuples of three ints (RGB format).  
Also you can change text font by using another font file and changing
path to it in `config.py` file in block "customization" in manual 
launching mode or in `.env` file if launching in Docker.  
Note that file must be TrueType or OpenType.  

### Animation

If you want to add background gif image you should place `.gif` file 
somewhere near the project and set path to it in `config.py` file in block 
"customization" or in `.env` file (`BG_GIF_PATH` variable).

### Time Zone

You should manually set time zone by changing value in `config.py` 
or in `.env` files (`TIME_ZONE` variable). List of all time zones you
can found 
[here](https://gist.github.com/heyalexej/8bf688fd67d7199be4a1682b3eec7568).

## Launching (with Docker) ##

First you should build the container:

```shell script
docker build --tag tg_avatar .
```

Next change variables in `.env` file and launch the container 
(you should launch it in `interactive` mode because of
Telegram validation code):

```shell script
docker run --restart always --env-file .env --interactive --name tg_avatar_container --network host tg_avatar
```

## License ##

	"THE BEERWARE LICENSE" (Revision 42):
	Andrey Bibea wrote this code. As long as you retain this 
	notice, you can do whatever you want with this stuff. If we
	meet someday, and you think this stuff is worth it, you can
	buy me a beer in return.