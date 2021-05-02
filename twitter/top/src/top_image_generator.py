# Image
from PIL import Image, ImageDraw, ImageFont
from typing import Final

# API
import requests

# Cloud
import boto3

# System
from datetime import date, datetime
import calendar
import io
import locale

NUMBER_OF_COINS: Final = 5
FIAT_COIN: Final = "USD"
MAX_DECIMALS: Final = 4

TEMPLATE: Final = {
    'daily': {
        'image': 'top-cryptos-template.png',
        'date': (70, 71, 98),
        'text': (43, 45, 66),
        'api': f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={FIAT_COIN.lower()}&order=volume_desc&per_page=6&page=1&sparkline=false&price_change_percentage=24h"
    },
    'weekly': {
        'image': 'top-cryptos-template-weekly.png',
        'date': (98, 70, 70),
        'text': (66, 43, 43),
        'api': f"https://api.coingecko.com/api/v3/coins/markets?vs_currency={FIAT_COIN.lower()}&order=market_cap_desc&per_page=5&page=1&sparkline=false"
    }
}

PROPERTIES: Final = {
    'y': 238,
    'symbol': {
        'x': 357.99,
        'font': 'Poppins-Black.ttf',
        'size': 22
    },
    'coin': {
        'x': 272,
        'bucketKey': 'crypto-icons'
    },
    'mktcap': {
        'x': 522,
        'font': 'Poppins-Light.ttf',
        'size': 18,
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


def get_data(current):
    response = requests.get(TEMPLATE[current]['api'])
    json_response = response.json()
    coin_info = list()

    for i in range(NUMBER_OF_COINS):
        if json_response[i]['symbol'] != "etlt":
            coin_info.append({
                'symbol': json_response[i]['symbol'].upper(),
                'price': f"{round(json_response[i]['current_price'], MAX_DECIMALS):,}",
                'change24hr': f"{round(json_response[i]['price_change_24h'], MAX_DECIMALS):,}",
                'mktcap': f"{round(json_response[i]['market_cap'], MAX_DECIMALS):,}"
            })
    return coin_info


def read_icon(bucket, coin):
    s3 = boto3.resource('s3', region_name='us-west-2')
    bucket = s3.Bucket(bucket)
    image_object = bucket.Object(f"crypto-icons/png/{coin}.png")
    response = image_object.get()
    file_stream = response['Body']
    return file_stream


def generate_image(top_type, bucket):
    locale.setlocale(locale.LC_ALL, 'es_ES')
    coins = get_data(top_type)

    Image.DEBUG = True
    image_template = Image.open(f"./static/img/{TEMPLATE[top_type]['image']}").convert("RGBA")
    image_draw = ImageDraw.Draw(image_template)
    image_draw.text(xy=(1186, 639.86),
                    text=get_date_text(),
                    anchor="rt",
                    fill=TEMPLATE[top_type]['date'],
                    align="right",
                    #font=ImageFont.truetype("./static/font/Poppins/Poppins-SemiBoldItalic.ttf", 18, encoding="unic")
                    )

    for index, coin in enumerate(coins, start=1):
        y = PROPERTIES['y'] + ((82.8 * (index - 1) if index > 2 else 82.8) if index > 1 else 0)

        image_draw.text(xy=(PROPERTIES['symbol']['x'], y),
                        text=f"${coin['symbol']}",
                        anchor="lt",
                        fill=TEMPLATE[top_type]['text'],
                        align="left",
                        #font=ImageFont.truetype(f"./static/font/Poppins/{PROPERTIES['symbol']['font']}",
                        #                        PROPERTIES['symbol']['size'])
                        )
        if top_type == "daily":
            image_draw.text(xy=(PROPERTIES['change24hr']['x'], y),
                            text=f"${coin['change24hr']}",
                            anchor="lt",
                            fill=TEMPLATE[top_type]['text'],
                            align="left",
                            #font=ImageFont.truetype(f"./static/font/Poppins/{PROPERTIES['change24hr']['font']}",
                            #                        PROPERTIES['change24hr']['size'])
            )

            if float(coin['change24hr'].replace(',', '').replace("−", "-")) < 0:
                image_template.paste(Image.open(PROPERTIES['change24hr']['down']['path']),
                                     (PROPERTIES['change24hr']['up']['x'],
                                      int(y) + 1))
            else:
                image_template.paste(Image.open(PROPERTIES['change24hr']['up']['path']),
                                     (PROPERTIES['change24hr']['up']['x'],
                                      int(y) + 2))
        elif top_type == "weekly":
            image_draw.text(xy=(PROPERTIES['mktcap']['x'], y),
                            text=f"${coin['mktcap']}",
                            anchor="lt",
                            fill=TEMPLATE[top_type]['text'],
                            align="left",
                            #font=ImageFont.truetype(f"./static/font/Poppins/{PROPERTIES['mktcap']['font']}",
                            #                        PROPERTIES['mktcap']['size'])
                            )

        coin_image = Image.open(read_icon(bucket, coin['symbol'].lower())).convert("RGBA")
        coin_image.thumbnail((72, 72))

        image_template.paste(coin_image, (PROPERTIES['coin']['x'], int(y) - 26), coin_image)

        image_draw.text(xy=(PROPERTIES['price']['x'], y),
                        text=f"${coin['price']}",
                        anchor="lt",
                        fill=TEMPLATE[top_type]['text'],
                        align="left",
                        #font=ImageFont.truetype(f"./static/font/Poppins/{PROPERTIES['price']['font']}",
                        #                        PROPERTIES['price']['size'])
                        )

    upload_image(image_template, top_type, bucket)


def upload_image(image_template, top_type, bucket):
    s3 = boto3.resource('s3', region_name='us-west-2')
    bucket = s3.Bucket(bucket)
    image_object = bucket.Object(f"top-images/{top_type}/{date.today()}.png")
    in_mem_file = io.BytesIO()
    image_template.save(in_mem_file, format("png"))
    image_object.put(Body=in_mem_file.getvalue())
