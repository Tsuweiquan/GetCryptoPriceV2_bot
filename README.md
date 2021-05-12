# GetCryptoPriceV2_bot
Mini project to obtain crypto prices from telegram via a bot. This uses AWS serverless architecture.

##Process Flow

1) Telegram message type "/BTC"
2) This will trigger a telegram webhook to call AWS API Gateway Rest API
3) AWS API Gateway will trigger a Lambda Function
4) Lambda function will run the code to obtain the crypto price
5) Lambda function will do a post request to telegram chat id that triggered the message
6) User will receive the Crypto price.
