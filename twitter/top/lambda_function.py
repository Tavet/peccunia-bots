# Native
import os
from datetime import date
from base64 import b64decode

# Cloud
import boto3

# Processors
from PIL import Image
import tweepy

# Modules
import top_image_generator as generator


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


def read_top_image(top_type):
    s3 = boto3.resource('s3', region_name='us-west-2')
    bucket = s3.Bucket(os.environ['ASSETS_BUCKET'])
    image_object = bucket.Object(f"top-images/{top_type}/{date.today()}.png")
    response = image_object.get()
    file_stream = response['Body']
    im = Image.open(file_stream)
    im.save("temp.png", format="png")


def lambda_handler(event, context):
    generator.generate_image(event['type'], event['bucket'])
    read_top_image(event['type'])
    tweet = event['message']
    return tweet_image(tweet)


def tweet_image(message):
    # twitter_api().update_with_media("./temp.png", message)
    return "Tweet publicado"


lambda_handler({
    "type": "weekly",
    "bucket":  "peccunia-assets",
    "message": "Top 5 Cryptos por Market Cap.\nEdición semanal.\n\n#crypto #bitcoin #cryptocurrency #blockchain #btc #ethereum #money #trading #entrepreneur #bitcoinmining #litecoin #bitcoins #investing #cryptocurrencies #bitcoinnews #eth #trader #investor #business #invest #success #investment"
}, None)
