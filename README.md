Peccunia Bots
======

### Table of Contents
1. [Twitter](#twitter)
    1. [Local Execution](#local-execution)
    2. [Possible Automated Tweets](#possible-automated-tweets)

**AWS Resources**

- *Assets Bucket* [peccunia-assets](https://s3.console.aws.amazon.com/s3/buckets/peccunia-assets?region=us-west-2&tab=objects)
- *KMS Key for Encryption/Decryption* [peccunia-bots-key](https://us-west-2.console.aws.amazon.com/kms/home?region=us-west-2#/kms/keys/fa57f222-b014-4262-8380-9b3b5a4bd551)


<div id="twitter" />

Twitter 
======

<div id="local-execution" />

Local Exectuion
------

- Add credentials to default.env
- Build the docker-compose file
- Make an HTTP request. E.g:
```bash
curl -XPOST "http://localhost:9000/2015-03-31/functions/function/invocations" -d '{"type": "weekly","bucket":  "peccunia-assets","message": "test"}'
```

<div id="possible-automated-tweets" />

Possible Automated Tweets
------

The following JSON properties are mapped in CloudWatch with a CRON job. The purpose of this CRON job is to execute the Lambda that generates the image in the indicated time with the following properties to post tweets.

#### Trending Top
```json
{
    "type": "trending",
    "bucket": "peccunia-assets",
    "message": "Top 5 Trending Cryptos.\nEdición diaria.\n\n#crypto #bitcoin #cryptocurrency #blockchain #btc #ethereum #money #trading #entrepreneur #bitcoinmining #litecoin #bitcoins #investing #cryptocurrencies #bitcoinnews #eth #trader #investor #business #invest #success #investment"
}
```

#### Daily Top
```json
{
    "type": "daily",
    "bucket": "peccunia-assets",
    "message": "Top 5 Cryptos por su volumen en las últimas 24 horas.\nEdición diaria.\n\n#btc #eth #criptomonedas #binance #exchange #investment #bnb #bitcoin #cryptocurrency #blockchain #ethereum #money #trading #bitcoinmining #cryptocurrencies"
}
```

#### Weekly Top
```json
{
    "type": "weekly",
    "bucket": "peccunia-assets",
    "message": "Top 5 Cryptos por Market Cap.\nEdición semanal.\n\n#crypto #bitcoin #cryptocurrency #blockchain #btc #ethereum #money #trading #entrepreneur #bitcoinmining #litecoin #bitcoins #investing #cryptocurrencies #bitcoinnews #eth #trader #investor #business #invest #success #investment"
}
```
