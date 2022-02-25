import json, config
from flask import Flask, request
from binance.client import Client
from binance.enums import *
import os
import pandas as pd
import notify as n

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

def round_down(value, decimals):
    factor = 1 / (10 ** decimals)
    val = (value // factor) * factor
    val = float("{:.5f}".format(val))
    return val

@app.route("/")
def hello_world():
    return "<p>HOME</p>"

@app.route("/test/ConfigAPIKey")
def testKey():
    return "<p>"+config.API_KEY+"</p>"

@app.route("/test/binance-notify",methods=['POST'])
def testNotifyBinance():
    return n.send_from_binance(request)

@app.route("/test/notify",methods=['POST'])#TODO -- change response to be from Binance
def testNotify():
    data = json.loads(request.data)

    #quantity_real = float(posSize())/data['strategy']['order_price']
    quantity_real = float(50)/data['strategy']['order_price']
    quantity_real = round_down(quantity_real, 5)

    side = data['strategy']['order_action'].upper()
    btc_amount = quantity_real
    price = data['strategy']['order_price']
    usdt_amount = btc_amount*price
    time = data['time']
    return n.send(side,btc_amount,price,usdt_amount,time)
   

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
    pair = data['ticker']
    
    quantity_real = float(posSize())/data['strategy']['order_price']
    quantity_real = round_down(quantity_real, 5)
    print("Coin quantity ", quantity_real)

    if side == "BUY":
        order_response = order(side, quantity_real, pair)
        print("Order response : ", order_response)
        print("Type of order response : ", type(order_response))
        if order_response:
            n.send_from_binance(order_response)
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
        quantity_sell = round_down(quantity_sell, 5)
        order_response = order(side, quantity_sell, pair)
        if order_response:
            n.send_from_binance(order_response)
            print("Order response : ", order_response)
            print("Type of order response : ", type(order_response))
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
