import hashlib
import hmac
import time
import requests
from dotenv import load_dotenv
import os

load_dotenv()

SUMSUB_APP_TOKEN = os.getenv("SUMSUB_APP_TOKEN")
SUMSUB_SECRET_KEY = os.getenv("SUMSUB_SECRET_KEY")
BASE_URL = "https://api.sumsub.com"
REQUEST_TIMEOUT = 60

def sign_request(request):
    prepared_request = request.prepare()
    now = int(time.time())
    method = request.method.upper()
    path_url = prepared_request.path_url
    body = b'' if prepared_request.body is None else prepared_request.body
    if isinstance(body, str):
        body = body.encode('utf-8')
    data_to_sign = str(now).encode('utf-8') + method.encode('utf-8') + path_url.encode('utf-8') + body
    signature = hmac.new(SUMSUB_SECRET_KEY.encode('utf-8'), data_to_sign, digestmod=hashlib.sha256)
    prepared_request.headers['X-App-Token'] = SUMSUB_APP_TOKEN
    prepared_request.headers['X-App-Access-Ts'] = str(now)
    prepared_request.headers['X-App-Access-Sig'] = signature.hexdigest()
    return prepared_request

def test(method, path):
    resp = sign_request(requests.Request(method, BASE_URL + path))
    s = requests.Session()
    response = s.send(resp, timeout=REQUEST_TIMEOUT)
    print(f"{method} {path} → {response.status_code}: {response.text[:200]}")
    print()

test("GET", "/resources/applicants/-;limit=5")
test("GET", "/resources/applicants?type=individual&reviewStatus=completed&limit=5")
test("POST", "/resources/applicants/-/list")
