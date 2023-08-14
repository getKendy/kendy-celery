from .celery import app
import os
import redis
import requests
import json
from kucoin.client import WsToken, Market
from kucoin.ws_client import KucoinWsClient
import asyncio
import time
from .fastapi import get_fastapi_token

kuclient = Market(url='https://api.kucoin.com')

collected_tickers = []
r = redis.Redis(host=os.environ.get('REDIS_CACHE'),
                port=os.environ.get('REDIS_PORT'),
                db=os.environ.get('REDIS_DBKUCOIN'),
                password=os.environ.get('REDIS_PASSWORD'))

def pop_all(list_input):
    '''remove all items from list'''
    result, list_input[:] = list_input[:], []
    return result

@app.task
def start_klines_ticker():
    data = r.get("KucoinRunning")
    if not data:
        start_websocket.delay()

@app.task
def get_symbols_from_exchangeinfo():
    '''get symbols from exchange_info'''
    exchange_info = kuclient.get_all_tickers()
    for symbol in exchange_info['ticker']:
        r.set(("marketKu" + symbol["symbol"]), str(json.dumps(symbol)), 86400)

@app.task
def ticker24h():
    exchange_info = kuclient.get_all_tickers()
    for tick in exchange_info['ticker']:
        # print(tick)
        if tick['changePrice'] is not None:
            symbol = tick['symbol'].split('-')[0] + tick['symbol'].split('-')[1]
            data = {
                'market': tick['symbol'],
                'symbol': symbol,
                'open': float(tick['last']) - float(tick['changePrice']),
                'high': tick['high'],
                'low': tick['low'],
                'close': tick['last'],
                'volume': tick['vol'],
                'quote': tick['volValue'],
            }
            # print(data)
            r.set(symbol, json.dumps(data), 86400)


@app.task
def start_websocket():
    symbols = kuclient.get_all_tickers()
    loop = asyncio.new_event_loop()
    loop.run_until_complete(websocketConnect(marketPairs=symbols['ticker']))


@app.task
async def websocketConnect(marketPairs):
    async def event(msg):
        r.set("KucoinRunning", "1", 120)
    # print(time.time())
    # print(msg["data"]["time"])
    # r.set("KucoinRunning", "1", 120)
    # print(msg)
        if len(collected_tickers) < 20:
            collected_tickers.append(msg)
        else:
            save_tickers.delay(tickers=collected_tickers)
            pop_all(list_input=collected_tickers)
            collected_tickers.append(msg)
    # Subscribe to ALL tickers
    publicClient = WsToken(url="https://api.kucoin.com")
    wsClientTick1 = await KucoinWsClient.create(None, publicClient, event, private=False)
    wsClientTick2 = await KucoinWsClient.create(None, publicClient, event, private=False)
    wsClientTick3 = await KucoinWsClient.create(None, publicClient, event, private=False)
    wsClientTick4 = await KucoinWsClient.create(None, publicClient, event, private=False)
    wsClientTick5 = await KucoinWsClient.create(None, publicClient, event, private=False)
    wsClientTick6 = await KucoinWsClient.create(None, publicClient, event, private=False)
    # r.set("KucoinRunning", "1", 305)

    watched_topics = []
    for ticker in marketPairs:
        if ticker['symbol'].split('-')[1] == "BTC" or ticker['symbol'].split('-')[1] == "USDT":
            # print(type(ticker))
            # print(ticker)
            # topic = "/market/ticker:all"
            topic = "/market/candles:" + ticker['symbol']  + "_1min"
            # print(topic)
            watched_topics.append(topic)
            
            # await wsClientTick.subscribe(topic)
            # await asyncio.sleep(0.4)
    # print(len(watched_topics))
    for x in range(len(watched_topics)):
        # print(watched_topics[x])
        # print(type(watched_topics[x]))
        if x < 250:
            await wsClientTick1.subscribe(watched_topics[x])
            await asyncio.sleep(0.3)
        elif x > 250 and x < 500:
            await wsClientTick2.subscribe(watched_topics[x])
            await asyncio.sleep(0.3)
        elif x > 500 and x < 750:
            await wsClientTick3.subscribe(watched_topics[x])
            await asyncio.sleep(0.3)
        elif x > 750 and x < 1000:
            await wsClientTick4.subscribe(watched_topics[x])
            await asyncio.sleep(0.3)
        elif x > 1000 and x < 1250:
            await wsClientTick5.subscribe(watched_topics[x])
            await asyncio.sleep(0.3)
        elif x > 1250 and x < 1500:
            await wsClientTick6.subscribe(watched_topics[x])
            await asyncio.sleep(0.3)
    while True:
        await asyncio.sleep(1)



@app.task
def save_tickers(tickers):
    all_tickers = []
    for ticker in tickers:
        # print(ticker)
        # print(type(ticker["data"]))
        all_tickers.append(
            {
                "date": ticker["data"]["candles"][0],
                "exchange": "kucoin",
                "symbol": ticker["data"]["symbol"].split("-")[0] + ticker["data"]["symbol"].split("-")[1],
                "market": ticker["data"]["symbol"].replace("-", "/"),
                # "market": ticker['s'],
                "close": ticker["data"]["candles"][2],
                "open": ticker["data"]["candles"][1],
                "high": ticker["data"]["candles"][3],
                "low": ticker["data"]["candles"][4],
                "volume": ticker["data"]["candles"][5],
                "quote": ticker["data"]["candles"][6],
            }
        )
    # enf for loop
    if len(all_tickers) >= 1:
        token = get_fastapi_token()
        if not token:
            return "no JWT"
        # print(token)
        # print(type(token))
        headers = {
            "Authorization": token['token_type'] + " " + token['access_token'],
            "Content-Type": "application/json",
            "accept": "application/json"
        }
        requests.post(
            os.environ.get('API') + "v2/tickers/", json=all_tickers, headers=headers)
    # print('saved')
