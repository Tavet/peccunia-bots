import os
import tweepy
import boto3
from base64 import b64decode
import top_image_generator as generator
from datetime import date
from PIL import Image
import numpy as np


def twitter_api():
    kms = boto3.client('kms')
    access_token = kms.decrypt(
        CiphertextBlob=b64decode(os.environ['ACCESS_TOKEN']),
        EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
    )['Plaintext'].decode('utf-8')
    access_token_secret = kms.decrypt(
        CiphertextBlob=b64decode(os.environ['ACCESS_TOKEN_SECRET']),
        EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
    )['Plaintext'].decode('utf-8')
    consumer_key = kms.decrypt(
        CiphertextBlob=b64decode(os.environ['CONSUMER_KEY']),
        EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
    )['Plaintext'].decode('utf-8')
    consumer_secret = kms.decrypt(
        CiphertextBlob=b64decode(os.environ['CONSUMER_SECRET']),
        EncryptionContext={'LambdaFunctionName': os.environ['AWS_LAMBDA_FUNCTION_NAME']}
    )['Plaintext'].decode('utf-8')

    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    return tweepy.API(auth)


def read_top_image():
    s3 = boto3.resource('s3', region_name='us-west-2')
    bucket = s3.Bucket('peccunia-top-images')
    image_object = bucket.Object(f"daily/volume-{date.today()}.png")
    response = image_object.get()
    file_stream = response['Body']
    im = Image.open(file_stream)
    return np.array(im)


def lambda_handler(event, context):
    generator.generate_image("daily")
    tweet = "Top 5 Cryptos por su volumen en las últimas 24 horas.\nEdición diaria.\n\n#btc #eth #criptomonedas " \
            "#binance #exchange #investment #usdt #binance #bitcoin #cryptocurrency #blockchain #btc #ethereum " \
            "#money #trading #bitcoinmining #cryptocurrencies"
    return tweet_image(read_top_image(), tweet)


def tweet_image(image_template, message):
    api = twitter_api()
    print(image_template)
    api.update_with_media(image_template, message)
    return "Tweet publicado"


lambda_handler(None, None)
