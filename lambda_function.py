#set the webhook: https://api.telegram.org/botXXXXX/setWebHook?url=https://XXXXXXX.execute-api.ap-southeast-1.amazonaws.com/Dev
#Updated on 12 May 2021
import json
import requests
import logging
import os

TELE_TOKEN = os.environ['TELE_TOKEN']
URL = "https://api.telegram.org/bot{}/".format(TELE_TOKEN)
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def send_message(text, chat_id):
    final_text = text
    url = URL + "sendMessage?text={}&chat_id={}".format(final_text, chat_id)
    requests.get(url)
    
def extractCode(text):
    coinCode = text.split('/')
    coinCode = coinCode[1].upper()
    return coinCode

def get_prices(coinCode):
    coins = []
    coins.append(coinCode)
    crypto_data = requests.get("https://min-api.cryptocompare.com/data/pricemultifull?fsyms={}&tsyms=USD".format(",".join(coins))).json()["RAW"]
    data = {}
    for i in crypto_data:
        data[i] = {
            "coin": i,
            "price": crypto_data[i]["USD"]["PRICE"],
            "change_day": crypto_data[i]["USD"]["CHANGEPCT24HOUR"],
            "change_hour": crypto_data[i]["USD"]["CHANGEPCTHOUR"]
         }
    return data

def format_OutputData(crypto_data):
    message = ""
    for i in crypto_data:
        coin = crypto_data[i]["coin"]
        price = crypto_data[i]["price"]
        change_day = crypto_data[i]["change_day"]
        change_hour = crypto_data[i]["change_hour"]
        message += f"Coin: {coin}\nPrice: ${price:,.8f}\nHour Change: {change_hour:.3f}%\nDay Change: {change_day:.3f}%\n\n"
    return message

# sample output
#{'update_id': 449465297, 'message': {'message_id': 5, 'from': {'id': 419502811, 'is_bot': False, 'first_name': 'Wei Quan', 'last_name': 'Tsu', 'username': 'tsuwq', 'language_code': 'en'}, 'chat': {'id': 419502811, 'first_name': 'Wei Quan', 'last_name': 'Tsu', 'username': 'tsuwq', 'type': 'private'}, 'date': 1620747951, 'text': 'sent at 11.45'}
def lambda_handler(event, context):
    logging.info(event)
    chat_id = event['message']['chat']['id']
    receivedText = event['message']['text']
    logging.info(receivedText)
    coinCode = extractCode(receivedText)
    obtainCoinData = get_prices(coinCode)
    beautifyMsg = format_OutputData(obtainCoinData)
    send_message(beautifyMsg, chat_id)
    logging.info(beautifyMsg)
    return {
        'statusCode': 200
    }

