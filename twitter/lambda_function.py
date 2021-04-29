import os
import tweepy
import boto3
from base64 import b64decode

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
    twitter_api().update_status("#CRYPTOS Peccunia Rules")
    return 'Tweet publicado'

