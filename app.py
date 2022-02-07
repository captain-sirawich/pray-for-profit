import json, config
from flask import Flask, request
from binance.client import Client
from binance.enums import *
import os
import pandas as pd

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

@app.route("/test1")
def test1():
    return "<p>TEST1 Duhh</p>"

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

@app.route("/test/posSize", methods=['POST'])
def posSize():
    client = Client(config.API_KEY,config.API_SECRET)
    info = client.get_account()
    df = pd.DataFrame(info["balances"])
    usdt = df[df["asset"]=="USDT"].to_dict('records')[0]

    data = json.loads(request.data)
    risk = data['strategy']['risk']
    slper = data['strategy']['slper']
    equity = float(usdt['free'])
    if equity < 1 :
        equity = 18998.3
    positionSize = equity*risk/slper
    print(positionSize)

    return str(positionSize)

@app.route("/test/webhook", methods=['POST'])
def testWebhook():
    data = json.loads(request.data)
    return "I got this data\n" + json.dumps(data)



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
