import os
import tweepy
import boto3
from base64 import b64decode
import top_image_generator as generator

kms = boto3.client('kms')


def twitter_api():
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


def lambda_handler(event, context):
    api = twitter_api()
    generator.generate_image("daily")
    media = api.media_upload("./top.png")
    tweet = "Top 5 Cryptos por su volumen en las últimas 24 horas.\nEdición diaria.\n\n#btc #eth #criptomonedas " \
            "#binance #exchange #investment #usdt #binance #bitcoin #cryptocurrency #blockchain #btc #ethereum " \
            "#money #trading #bitcoinmining #cryptocurrencies"
    api.update_status(status=tweet, media_ids=[media.media_id])
    return 'Tweet publicado'


lambda_handler(None, None)
