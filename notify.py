import requests
import json,config
from dateutil import parser
from datetime import datetime, timedelta, timezone


url = 'https://notify-api.line.me/api/notify'
token = config.NOTIFY_KEY
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}

def timeParser(d):
    yourdate = parser.parse(str(d))
    tz = timezone(timedelta(hours=7))
    t=yourdate.astimezone(tz)
    formatted_time = t.strftime("%H:%M:%S, %m/%d/%Y")
    return formatted_time

def send(side,btc_amount,price,usdt_amount,time):
    if(side == "BUY"):
        line1 = f"The Bot just bought : {btc_amount} BTC"
        line2 = f"At Price : {price} USDT"
        line3 = f"For {usdt_amount} USDT"
    elif (side == "SELL"):
        line1 = f"The Bot just sold : {btc_amount} BTC"
        line2 = f"At Price : {price} USDT"
        line3 = f"For : {usdt_amount} USDT"

    t = timeParser(time)
    line4 = f"Time : {t}"
    message = f"\n{line1} 🚀🚀🚀\n{line2}\n{line3}\n{line4}"
    r = requests.post(url, headers=headers , data = {'message':message})
    print (r.text)
    return r.text

def send_from_binance(request):
    data = request
    fills = data['fills']
    price = float(fills[0]['price'])
    qty = 0
    for fill in fills:
        qty+= float(fill['qty'])

    side = data['side']
    usdt_amount = qty*price
    timestamp = data['transactTime']
    time = datetime.fromtimestamp(timestamp / 1e3)
   
    return send(side,qty,price,usdt_amount,time)

mock_dict ={"symbol": "BTCUSDT", "orderId": 9545821217, "orderListId": -1, "clientOrderId": "uiSutt5vNa2lalB78yP16r", "transactTime": 1645797601593, "price": "0.00000000", "origQty": "0.00035000", "executedQty": "0.00035000", "cummulativeQuoteQty": "13.77425000", "status": "FILLED", "timeInForce": "GTC", "type": "MARKET", "side": "BUY", "fills": [{"price": "39355.00000000", "qty": "0.00035000", "commission": "0.00000035", "commissionAsset": "BTC", "tradeId": 1269860910}]}