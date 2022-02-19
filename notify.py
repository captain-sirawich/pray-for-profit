import requests
import config

url = 'https://notify-api.line.me/api/notify'
token = config.NOTIFY_KEY
headers = {'content-type':'application/x-www-form-urlencoded','Authorization':'Bearer '+token}



def send(message):
    r = requests.post(url, headers=headers , data = {'message':message})
    print (r.text)
    return r.text