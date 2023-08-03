from .celery import app
import os
import redis
import requests
import json

r = redis.Redis(host=os.environ.get('REDIS_CACHE'),
                port=os.environ.get('REDIS_PORT'),
                db=os.environ.get('REDIS_DB'),
                password=os.environ.get('REDIS_PASSWORD'))

def set_fastapi_token(username, password):
    # url = 'http://10.20.31.145:8000/api/v2/login'
    url = os.environ.get('API') + 'v2/login'
    response = requests.request("POST", url, data={"username": username, "password": password})
    token = response.json()
    if not token:
        return json.loads({'access_token': 'ERROR', 'token_type': 'ERROR'})
    r.set('fastapi_token', response.text, (1420 * 60 * 60))
    return response.json()

@app.task
def get_fastapi_token():
    token = r.get('fastapi_token')
    if not token:
        return set_fastapi_token('ron', 'Oldsch00l')
    # print(token)
    return json.loads(token)

  