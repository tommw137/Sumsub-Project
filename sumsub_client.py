import hashlib
import hmac
import time
import requests
from dotenv import load_dotenv
import os

load_dotenv()

SUMSUB_APP_TOKEN = os.getenv("SUMSUB_APP_TOKEN")
SUMSUB_SECRET_KEY = os.getenv("SUMSUB_SECRET_KEY")
BASE_URL = os.getenv("SUMSUB_BASE_URL")
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

def make_request(method, url_path, body=None):
    req = requests.Request(method, BASE_URL + url_path)
    if body:
        req.json = body
    resp = sign_request(req)
    s = requests.Session()
    response = s.send(resp, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    return response.json()

if __name__ == "__main__":
    # search for applicants using POST
    result = make_request("POST", "/resources/applicants/search", body={"limit": 10, "offset": 0})
    print(result)
