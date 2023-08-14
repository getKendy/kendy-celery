from .celery import app
from binance.spot import Spot as SpotClient
from binance.websocket.spot.websocket_client import SpotWebsocketClient as WebSocketClient
import time
import redis
import os
import requests
import json
from .fastapi import get_fastapi_token

collected_tickers = []
r = redis.Redis(host=os.environ.get('REDIS_CACHE'),
                port=os.environ.get('REDIS_PORT'),
                db=os.environ.get('REDIS_DBBINANCE'),
                password=os.environ.get('REDIS_PASSWORD'))


def pop_all(list_input):
    '''remove all items from list'''
    result, list_input[:] = list_input[:], []
    return result

@app.task
def start_klines_ticker():
    data = r.get("BinanceTickerRunning")
    if not data:
        get_klines_all_symbols.delay()
        
@app.task
def get_exchange_info():
    '''get exchange info'''
    spot_client = SpotClient()
    exchange_info = spot_client.exchange_info()
    return exchange_info


@app.task
def get_symbols_from_exchangeinfo():
    '''get symbols from exchange_info'''
    exchange_info = get_exchange_info()
    for symbol in exchange_info['symbols']:
        r.set(("marketBin" + symbol["symbol"]), str(json.dumps(symbol)), 86400)


@app.task
def get_klines_all_symbols():
    '''get klines all symbols'''
    # all_symbols = get_symbols_from_exchangeinfo()
    # time.sleep(5)
    # if len(all_symbols) > 4000:
    #     return {'error': 'not enough clients to open all kline streams'}
    try:
        get_symbols_from_exchangeinfo.delay()
        ws_miniticker = WebSocketClient()
        ws_miniticker.start()
        print('miniticker started')
        time.sleep(1)
        ws_client1 = WebSocketClient()
        ws_client1.start()
        print('client1 started')
        time.sleep(1)
        ws_client2 = WebSocketClient()
        ws_client2.start()
        print('client2 started')
        time.sleep(1)
        ws_client3 = WebSocketClient()
        ws_client3.start()
        print('client3 started')
        time.sleep(1)
        ws_client4 = WebSocketClient()
        ws_client4.start()
        print('client4 started')
        time.sleep(1)
        
        # start kline test sockets
        # ws_client1.kline("BTCBUSD", id=251,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client2.kline("ETHBTC", id=3,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client2.kline("BNBBTC", id=4,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client2.kline("BNBETH", id=5,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client2.kline("PAXGBTC", id=6,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client2.kline("CAKEBTC", id=7,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client2.kline("ADABTC", id=8,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client2.kline("DOTBTC", id=9,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client2.kline("SOLBTC", id=10,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client2.kline("MATICBTC", id=11,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client2.kline("ATOMBTC", id=12,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client2.kline("LINKBTC", id=13,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client1.kline("ETHBUSD", id=252,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client1.kline("BNBBUSD", id=253,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client1.kline("BTCUSDT", id=16,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client1.kline("ETHUSDT", id=17,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client1.kline("BNBUSDT", id=18,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client1.kline("PAXGUSDT", id=19,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client1.kline("CAKEUSDT", id=20,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client1.kline("ADAUSDT", id=21,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client1.kline("DOTUSDT", id=22,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client1.kline("SOLUSDT", id=23,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client1.kline("MATICUSDT", id=24,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client1.kline("ATOMUSDT", id=25,interval='1m', callback=kline_message_collector)
        # time.sleep(0.25)
        # ws_client1.kline("LINKUSDT", id=26,interval='1m', callback=kline_message_collector)

        # minitticker
        ws_miniticker.mini_ticker(
            id=1,
            callback=miniticker_message_handler,
        )
        
        # # btc 1m klines for alerts
        btc_martkets = []
        keys = r.keys("marketBin*")
        for key in keys:
            market = dict(json.loads(r.get(key)))
            if market['quoteAsset'] == 'BTC':
                btc_martkets.append(market['symbol'])
        for x in range(len(btc_martkets)):
            if x < 250:
                ws_client1.kline(btc_martkets[x], id=x,
                                 interval='1m', callback=kline_message_collector)
                time.sleep(0.3)
            elif x > 250 and x < 500:
                ws_client2.kline(btc_martkets[x], id=x,
                                 interval='1m', callback=kline_message_collector)
                time.sleep(0.3)
            elif x > 500 and x < 750:
                ws_client3.kline(btc_martkets[x], id=x,
                                 interval='1m', callback=kline_message_collector)
                time.sleep(0.3)
            else:
                ws_client4.kline(btc_martkets[x], id=x,
                                 interval='1m', callback=kline_message_collector)
        
        
        
        #         time.sleep(0.25)
        # time.sleep(3600)
        # print('KeyboardInterrupt')
        # ws_client1.stop()
        # time.sleep(1)
        # ws_client2.stop()
        # time.sleep(1)
        # ws_client3.stop()
        # time.sleep(1)
        # ws_client4.stop() # logging.debug("closing ws connection")

   
        
        
    except KeyboardInterrupt:
        print('KeyboardInterrupt')
        ws_client1.stop()
        time.sleep(1)
        ws_client2.stop()
        time.sleep(1)
        ws_client3.stop()
        time.sleep(1)
        ws_client4.stop() # logging.debug("closing ws connection")
    except:
        print('Ticker ERROR')
        print('Ticker ERROR')
        print('Ticker ERROR')
        print('Ticker ERROR')
        print('Ticker ERROR')
        print('Ticker ERROR')
        print('Ticker ERROR')
        print('Ticker ERROR')
        print('Ticker ERROR')
        print('Ticker ERROR')
   
@app.task
def miniticker_message_handler(message):
    '''process miniticker message'''
    # print(message)
    # print(len(message))
    try:
        for tick in message:
            # print(tick)
            if tick['e'] == '24hrMiniTicker':
                try:
                    symbol = dict(json.loads(r.get("marketBin" + tick["s"])))
                except:
                    symbol = {"symbol": "noData"}
                key = str(tick["s"]).encode("UTF-8")
                # print(key)
                r.set(
                    key,
                    str(
                        json.dumps(
                            {
                                "symbol": tick["s"],
                                # "market": symbol["symbol"],
                                # "market": symbol["baseAsset"] + '-' + symbol["quoteAsset"],
                                "market": tick['s'],
                                "c": tick["c"],
                                "o": tick["o"],
                                "h": tick["h"],
                                "l": tick["l"],
                                "v": tick["v"],
                                "q": tick["q"],
                            }
                        )
                    ),
                    86400,   # 1 day
                )
    except TypeError as error:
        print(error)
    except KeyError as error:
        print(error)

@app.task
def kline_message_collector(message):
    '''process incoming ticker message'''
    # Collect multiple messages and send to task
    # print(message)
    if len(collected_tickers) < 20:
        collected_tickers.append(message)
        # print(len(collected_tickers))
    else:
        pre_process_tickers.delay(collected_tickers)
        # print(len(collected_tickers))
        pop_all(list_input=collected_tickers)
        # print(len(collected_tickers))
        collected_tickers.append(message)


@app.task
def pre_process_tickers(tickers):
    ''' pre processor for incoming tickers'''
    processed_tickers = []
    # print(tickers)
    # print(len(tickers))
    for ticker in tickers:
        try:
          if ticker["e"] == "kline":
            processed_tickers.append(ticker)
            # print(ticker)
        except:
            
            print({'error':ticker})
            # print('An exception occurred')
    if len(processed_tickers) > 0:
        save_tickers.delay(tickers=processed_tickers)


@app.task
def save_tickers(tickers):
    '''save tickers'''
    # print(tickers)
    # print(len(tickers))
    all_tickers = []
    for ticker in tickers:
        # print(ticker)
        # print(type(ticker))
        
        try:
            symbol = dict(json.loads(r.get("marketBin" + ticker["s"])))
        except:
            symbol = {"symbol": {"baseAsset":'noData',"quoteAsset":'noData'}}
        
        
        
        # print(ticker)
        # key = str(ticker["s"]).encode("UTF-8")
        # # print(key)
        # r.set(
        #     key,
        #     str(
        #         json.dumps(
        #             {
        #                 "symbol": ticker["s"],
        #                 # "market": symbol["symbol"],
        #                 "market": symbol["baseAsset"] + '/' + symbol["quoteAsset"],
        #                 "market": ticker['s'],
        #                 "c": ticker['k']["c"],
        #                 "o": ticker['k']["o"],
        #                 "h": ticker['k']["h"],
        #                 "l": ticker['k']["l"],
        #                 "v": ticker['k']["v"],
        #                 "q": ticker['k']["q"],
        #             }
        #         )
        #     ),
        #     60,
        # )
        all_tickers.append(
            {
                "date": ticker["E"],
                "exchange": "binance",
                "symbol": ticker["s"],
                "market": symbol["baseAsset"] + '/' + symbol["quoteAsset"],
                # "market": ticker['s'],
                "close": ticker['k']["c"],
                "open": ticker['k']["o"],
                "high": ticker['k']["h"],
                "low": ticker['k']["l"],
                "volume": ticker['k']["v"],
                "quote": ticker['k']["q"],
            }
        )
    # enf for loop
    r.set("BinanceTickerRunning", "1", 120)
    token = get_fastapi_token()
    if not token:
        return "no JWT"
    headers = {
        "Authorization": token['token_type'] + " " + token['access_token'],
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    # tickers = all_tickers
    if len(all_tickers) >= 1:
        requests.post(
            os.environ.get('API') + "v2/tickers/", json=all_tickers, headers=headers)



@app.task
def clean_old_tickers():
    '''clean old tickers'''
    # page = 1
    # i = 0
    # cleaning = True
    # while cleaning:
    token = get_fastapi_token()
    if not token:
        return "no JWT"
    headers = {
        "Authorization": token['token_type'] + " " + token['access_token'],
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    response = requests.get(
        os.environ.get('API') + 'v2/tickerexpired/2', headers=headers)
    if not response:
        return 'error'
    return response.json()
    
@app.task
def clean_old_alerts():
    '''clean old alerts'''
    # page = 1
    # i = 0
    # cleaning = True
    # while cleaning:
    token = get_fastapi_token()
    if not token:
        return "no JWT"
    headers = {
        "Authorization": token['token_type'] + " " + token['access_token'],
        "Content-Type": "application/json",
        "accept": "application/json"
    }
    response = requests.get(
        os.environ.get('API') + 'v2/alertexpired/24', headers=headers)
    if not response:
        return 'error'
    return response.json()