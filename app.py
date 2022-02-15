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

@app.route("/test/ConfigAPIKey")
def testKey():
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

@app.route("/test/getCoin")
def getCoin():
    client = Client(config.API_KEY,config.API_SECRET)
    info = client.get_account()
    data = pd.DataFrame(info["balances"])
    btc = data[data["asset"]=="BTC"].to_dict('records')[0]
    print("Coin on acc", btc)
    return btc

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
    
    positionSize = equity*risk/slper
    if positionSize > equity:
        positionSize = equity
        
    print("Position Size ", positionSize)

    return str(positionSize)

@app.route("/webhook", methods=['POST'])
def test_wh():
    data = json.loads(request.data)
    
    if data['passphrase'] != config.WEBHOOK_PASSPHRASE:
        return {
        "code": "fail",
        "wrong passphrase": data['passphrase']
        }
    
    side = data['strategy']['order_action'].upper()
    # quantity = data['strategy']['order_contracts']
    pair = data['ticker']
    
    quantity_real = float(posSize())/data['strategy']['order_price']
    quantity_real = round(quantity_real, 8)
    print("Coin quantity ", quantity_real)
    # return "test quantity"

    if side == "BUY":
        order_response = order(side, quantity_real, pair)
        if order_response:
            return {
                "code": "buy success",
                "message": "order executed"
            }
        else:
            print("order failed")

            return {
                "code": "buy error",
                "message": "order failed"
            }
    else:
        coin = getCoin()
        quantity_sell = float(coin['free'])
        quantity_sell = round(quantity_sell, 8)
        order_response = order(side, quantity_sell, pair)
        if order_response:
            return {
                "code": "sell success",
                "message": "order executed"
            }
        else:
            print("order failed")

            return {
                "code": "sell error",
                "message": "order failed"
            }
