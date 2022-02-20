import requests
import config

url = 'https://notify-api.line.me/api/notify'
token = config.NOTIFY_KEY
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}



def send(side,btc_amount,price,usdt_amount,time):
    if(side == "buy"):
        line1 = f"The Bot just bought : {btc_amount} BTC"
        line2 = f"At Price : {price} USDT"
        line3 = f"For {usdt_amount} USDT"
    else:
        line1 = f"The Bot just sold : {btc_amount} BTC"
        line2 = f"At Price : {price} USDT"
        line3 = f"For : {usdt_amount} USDT"

    line4 = f"Time : {time}"
    message = f"\n{line1}🚀🚀🚀\n{line2}\n{line3}\n{line4}"
    r = requests.post(url, headers=headers , data = {'message':message})
    print (r.text)
    return r.text