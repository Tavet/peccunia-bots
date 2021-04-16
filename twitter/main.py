from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import requests
import locale
import calendar
from typing import Final

NUMBER_OF_COINS: Final = 5
FIAT_COIN: Final = "USD"
MAX_DECIMALS: Final = 4

PROPERTIES: Final = {
    'y': 238,
    'symbol': {
        'x': 357.99,
        'font': 'Poppins-Black.ttf',
        'size': 22
    },
    'coin': {
        'x': 272,
        'path': './static/img/coins/'
    },
    'change24hr': {
        'x': 575,
        'font': 'Poppins-Light.ttf',
        'size': 18,
        'up': {
            'x': 545,
            'path': './static/img/up.png'
        },
        'down': {
            'x': 545,
            'path': './static/img/down.png'
        }
    },
    'price': {
        'x': 782,
        'font': 'Poppins-Light.ttf',
        'size': 18
    }
}


def get_date_text():
    today = datetime.today()
    return f"{today.day} de {calendar.month_name[today.month].capitalize()}. {today.year}"


def get_data():
    response = requests.get(f"https://min-api.cryptocompare.com/data/top/totalvolfull?limit=10&tsym={FIAT_COIN}",
                            headers={"Apikey": "d6df8f92f6e494fb1ae92a4672b2f68b9d548986ef869911fd781ada322796e0"})
    json_response = response.json()
    coin_info = list()

    for i in range(NUMBER_OF_COINS):
        coin_info.append({
            'symbol': json_response['Data'][i]['CoinInfo']['Name'],
            'price': f"{round(json_response['Data'][i]['RAW'][FIAT_COIN]['PRICE'], MAX_DECIMALS):,}",
            'change24hr': f"{round(json_response['Data'][i]['RAW'][FIAT_COIN]['CHANGE24HOUR'], MAX_DECIMALS):,}"
        })
    return coin_info


if __name__ == '__main__':
    locale.setlocale(locale.LC_ALL, 'es_ES')
    coins = get_data()
    get_date_text()

    image_template = Image.open('./static/img/top-cryptos-template.png').convert("RGBA")
    image_draw = ImageDraw.Draw(image_template)
    image_draw.text(xy=(1186, 639.86),
                    text=get_date_text(),
                    anchor="rt",
                    fill=(70, 71, 98),
                    align="right",
                    font=ImageFont.truetype("./static/font/Poppins/Poppins-SemiBoldItalic.ttf", 18))

    for index, coin in enumerate(coins, start=1):
        y = PROPERTIES['y'] + ((82.8 * (index - 1) if index > 2 else 82.8) if index > 1 else 0)

        image_draw.text(xy=(PROPERTIES['symbol']['x'], y),
                        text=f"${coin['symbol']}",
                        anchor="lt",
                        fill=(43, 45, 66),
                        align="left",
                        font=ImageFont.truetype(f"./static/font/Poppins/{PROPERTIES['symbol']['font']}",
                                                PROPERTIES['symbol']['size']))

        image_draw.text(xy=(PROPERTIES['change24hr']['x'], y),
                        text=f"${coin['change24hr']}",
                        anchor="lt",
                        fill=(43, 45, 66),
                        align="left",
                        font=ImageFont.truetype(f"./static/font/Poppins/{PROPERTIES['change24hr']['font']}",
                                                PROPERTIES['change24hr']['size']))

        import numpy as np
        coin_image = Image.open(f"{PROPERTIES['coin']['path']}{coin['symbol'].lower()}.png").convert("RGBA")
        coin_image.thumbnail((72, 72))

        image_template.paste(coin_image, (PROPERTIES['coin']['x'], int(y) - 26), coin_image)

        if float(coin['change24hr']) < 0:
            image_template.paste(Image.open(PROPERTIES['change24hr']['down']['path']),
                                 (PROPERTIES['change24hr']['up']['x'],
                                  int(y) + 1))
        else:
            image_template.paste(Image.open(PROPERTIES['change24hr']['up']['path']),
                                 (PROPERTIES['change24hr']['up']['x'],
                                  int(y) + 2))

        image_draw.text(xy=(PROPERTIES['price']['x'], y),
                        text=f"${coin['price']}",
                        anchor="lt",
                        fill=(43, 45, 66),
                        align="left",
                        font=ImageFont.truetype(f"./static/font/Poppins/{PROPERTIES['price']['font']}",
                                                PROPERTIES['price']['size']))

    image_template.save("top.png", format="png")
