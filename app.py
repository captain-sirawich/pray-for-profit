import json, config
from flask import Flask, request
from binance.client import Client
from binance.enums import *
import os

app = Flask(__name__)

app.config['ENV'] = 'development'
app.config['DEBUG'] = True
app.config['TESTING'] = True

client = Client(config.API_KEY, config.API_SECRET, tld='com')

def order(side, quantity, symbol, order_type=ORDER_TYPE_MARKET):
    try:
        print(f"sending order {order_type} - {side} {quantity} {symbol}")
        order = client.create_order(symbol=symbol, side=side, type=order_type, quantity=quantity)
    except Exception as e:
        print("an exception occured - {}".format(e))
        return False

    return order

@app.route("/")
def hello_world():
    return "<p>HOME</p>"

@app.route("/testConfigKey")
def test2():
    return "<p>"+config.API_KEY+"</p>"

@app.route("/test/getAccount")
def getAccount():
    client = Client(config.API_KEY,config.API_SECRET)
    info = client.get_account()
    data = pd.DataFrame(info["balances"])
    usdt = data[data["asset"]=="USDT"]
    btc = data[data["asset"]=="BTC"]
    print(usdt)
    print(btc)
    return info

@app.route("/webhook", methods=['POST'])
def test_wh():
    data = json.loads(request.data)
    
    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
        "code": "fail",
        "wrong passphrase": data['passphrase']
        }
    
    side = data['strategy']['order_action'].upper()
    quantity = data['strategy']['order_contracts']
    pair = data['ticker']
    order_response = order(side, quantity, pair)

    if order_response:
        return {
            "code": "success",
            "message": "order executed"
        }
    else:
        print("order failed")

        return {
            "code": "error",
            "message": "order failed"
        }
