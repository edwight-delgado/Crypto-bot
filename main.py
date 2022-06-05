from asyncio import events
from curses import keyname
from urllib import response
import requests, time
from datetime import date
import json

file = open("PRIVATE.json", 'r')


content = json.load(file)

IFTTT_KEY= content["KEYS"][0]["IFTTT_KEY"]
uri_api_cryto = content["APIS"][0]["CRYTO"]
BITCOIN_PRICE_THRESHOLD = 10000  # Set this to whatever you like

#ifttt_webhook_url = f'https://maker.ifttt.com/trigger/test_event/with/key/{your_key_is}'
#requests.post(ifttt_webhook_url)

def format_bitcoin_history(bitcoin_history):
    rows = []
    for bitcoin_price in bitcoin_history:
        # Formats the date into a string: '24.02.2018 15:09'
        date = bitcoin_price['date'].strftime('%d.%m.%Y %H:%M')

        price = bitcoin_price['price']
        # <b> (bold) tag creates bolded text
        # 24.02.2018 15:09: $<b>10123.4</b>
        row = '{}: $<b>{}</b>'.format(date, price)
        rows.append(row)

    # Use a <br> (break) tag to create a new line
    # Join the rows delimited by <br> tag: row1<br>row2<br>row3
    return '<br>'.join(rows)

def get_latest_bitcoin_price():
    response = requests.get(uri_api_cryto)
    res_json =  response.json()

    price_coins = {price_coins["id"]:price_coins["price"] for price_coins in res_json['coins']}
    return price_coins
def post_ifttt_webhook(event, value):
    # The payload that will be sent to IFTTT service
    data = {'value1': value}
    IFTTT_WEBHOOKS_URL = f"https://maker.ifttt.com/trigger/{event}/with/key/{IFTTT_KEY}"
    #ifttt_event_url = IFTTT_WEBHOOKS_URL.format(event,IFTTT_KEY)
    # Sends a HTTP POST request to the webhook URL
    print('msg send ')
    requests.post(IFTTT_WEBHOOKS_URL, json=data)

def main():
    bitcoin_history = []
    while True:
        price = get_latest_bitcoin_price()
        today = date.today()
        bitcoin_history.append({'date': today, 'price': price["bitcoin"]})

        # Send an emergency notification
        if price['bitcoin'] < BITCOIN_PRICE_THRESHOLD:
            post_ifttt_webhook('bitcoin_price_emergency', price["bitcoin"])

        # Send a Telegram notification
        # Once we have 5 items in our bitcoin_history send an update
        if len(bitcoin_history) == 5:
            post_ifttt_webhook('bitcoin_price_update', 
                               format_bitcoin_history(bitcoin_history))
            # Reset the history
            bitcoin_history = []

        # Sleep for 5 minutes 
        # (For testing purposes you can set it to a lower number)
        print(price['bitcoin'],today)
        minutes = 1 * 60
        time.sleep(minutes)


if __name__ == '__main__':
    print("Key: Value")
    content = json.load(file)
    print(content["KEYS"][0]["IFTTT_KEY"])
    #assert yaml_content['IFTTT_KEY'] 
    #print(content['KEYS'])

    #main()