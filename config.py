import os
#need this import when running on windows for some reason
from dotenv import load_dotenv

load_dotenv()
WEBHOOK_PASSPHRASE = "qwer1234"

API_KEY = os.getenv('HRK_KEY')
API_SECRET = os.getenv('HRK_SECRET')
NOTIFY_KEY = os.getenv('NOTIFY_KEY')