import requests
import config
from dateutil import parser
from datetime import datetime, timedelta, timezone


url = 'https://notify-api.line.me/api/notify'
token = config.NOTIFY_KEY
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}



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

def timeParser(d):
    yourdate = parser.parse(d)
    tz = timezone(timedelta(hours=7))
    t=yourdate.astimezone(tz)
    formatted_time = t.strftime("%H:%M:%S, %m/%d/%Y")
    return formatted_time
