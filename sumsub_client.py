import hmac
import hashlib
import time
import requests
from dotenv import load_dotenv
import os

load_dotenv()

APP_TOKEN = os.getenv("SUMSUB_APP_TOKEN")
SECRET_KEY = os.getenv("SUMSUB_SECRET_KEY")
BASE_URL = os.getenv("SUMSUB_BASE_URL")

def sign_request(secret_key, method, url_path, body=b""):
    timestamp = str(int(time.time()))
    message = timestamp.encode() + method.encode() + url_path.encode() + body
    signature = hmac.new(secret_key.encode(), message, hashlib.sha256).hexdigest()
    return timestamp, signature

def make_request(method, url_path, body=b""):
    timestamp, signature = sign_request(SECRET_KEY, method, url_path, body)
    
    headers = {
        "X-App-Token": APP_TOKEN,
        "X-App-Access-Ts": timestamp,
        "X-App-Access-Sig": signature,
        "Content-Type": "application/json"
    }
    
    url = BASE_URL + url_path
    response = requests.request(method, url, headers=headers, data=body)
    response.raise_for_status()
    return response.json()
