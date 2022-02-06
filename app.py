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

@app.route("/test1")
def test1():
    return "<p>TEST1</p>"
@app.route("/test2")
def test1():
    key = os.getenv("HRK_KEY")
    return "<p>" + key +"</p>"

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
