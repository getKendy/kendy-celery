# from .celery import app, candle_alert
from .celery import app
import pandas as pd
import pandas_ta as ta
import redis
import os
import requests
import json
# import socketio

r = redis.Redis(host=os.environ.get('REDIS_CACHE'),
                port=os.environ.get('REDIS_PORT'),
                db=os.environ.get('REDIS_DB'))

from appwrite.client import Client
from appwrite.services.databases import Databases

client = Client()
(client
  .set_endpoint(os.environ.get('APPWITE_ENDPOINT')) # Your API Endpoint
  .set_project(os.environ.get('APPWRITE_PROJECTID')) # Your project ID
  .set_key(os.environ.get('APPWRITE_KEY')) # Your secret API key
)
databases = Databases(client)

@app.task
def build_indicators_from_candles(timeframe,resample_frame):
    '''build indicators from candles'''
    # dateNow = datetime.datetime.now()
    # queryTime = datetime.datetime.now() - datetime.timedelta(minutes=30)
    # tableTickers = Tickers.objects.all().filter(date__gte=queryTime)
    # tableTickers = indicatorTickers([queryTime, dateNow])
   
    keys = r.keys("market*")
    for key in keys:
        # only btc pairs for now!!
        market = dict(json.loads(r.get(key)))
        if market["quoteAsset"] != "BTC":
            continue
        volume_24h = volume_24h_check(baseAsset=market['baseAsset'],quoteAsset=market["quoteAsset"])
        if  volume_24h > 150: 
            process_alert_ticker_data.delay(market=market,volume_24h=volume_24h,timeframe=timeframe,resample_frame=resample_frame,base=market['baseAsset'],quote=market['quoteAsset'])

@app.task
def process_alert_ticker_data(market,volume_24h,timeframe,resample_frame,base,quote):
    '''process alert ticker data'''
    try:
        response = requests.get(
                os.environ.get('API') + 'v2/tickers/' + market["symbol"])
        if not response:
            exit
        ticker_data = response.json()
        last_ticker = ticker_data[-1]
        # print({last_ticker['symbol']:'generating indicators'})
        
        df = pd.DataFrame(
            ticker_data,
            columns=[
                "id",
                "date",
                "symbol",
                "market",
                "close",
                "open",
                "high",
                "low",
                "volume",
                "quote",
            ],
        )
        df['DateTime'] = pd.to_datetime(df['date'])
        # print('creating index')
        df = df.set_index('DateTime')
        # print('dropping date')
        df = df.drop(['date'], axis=1)
        # !!!! RESAMPLE TICKERS INTO USABLE TIMEFRAMES
        df = df.resample(resample_frame, label='right', closed='right').agg({
            'open': 'first',
            'high': 'max',
            'low': 'min',
            'close': 'last',
            'volume': 'last',
            'quote': 'last'
        })
        # help(ta.bbands)
        df.ta.bbands(
            close=df["close"],
            length=20,
            std=2,
            mamode="sma",
            cumulative=True,
            append=True,
        )
        # print(df.tail(n=20))
       
        if (
            float(df.iloc[-1, df.columns.get_loc("close")])
            < float(df.iloc[-1, df.columns.get_loc("BBL_20_2.0")])
            and float(df.iloc[-1, df.columns.get_loc("BBB_20_2.0")]) >= 0.75    # min % BB width
        ):
            # help(ta.stoch)
            df.ta.stoch(
                high=df["high"],
                low=df["low"],
                smooth_k=1,
                cumulative=True,
                append=True,
            )
            
            # print(df.tail(n=20))
            
            if float(df.iloc[-1, df.columns.get_loc("STOCHk_14_3_1")]) < 20:
                trend24h = trend_24h_check(baseAsset=base,quoteAsset=quote)
                data = {
                    "date": last_ticker['date'],
                    "timeframe": timeframe,
                    "symbol": last_ticker['symbol'],
                    "market": last_ticker['market'],
                    "close": format(round(df.iloc[-1, df.columns.get_loc("close")], 8),'.8f'),
                    "volume": round(df.iloc[-1, df.columns.get_loc("volume")], 2),
                    "quote": round(df.iloc[-1, df.columns.get_loc("quote")], 2),
                    "volume24h": round(volume_24h,2),
                    "trend24h": trend24h,
                    "bbl": format(round(df.iloc[-1, df.columns.get_loc("BBL_20_2.0")], 8),'.8f'),
                    "bbm": format(round(df.iloc[-1, df.columns.get_loc("BBM_20_2.0")], 8),'.8f'),
                    "bbu": format(round(df.iloc[-1, df.columns.get_loc("BBU_20_2.0")], 8),'.8f'),
                    "bbb": round(df.iloc[-1, df.columns.get_loc("BBB_20_2.0")], 1),
                    "stochk": round(df.iloc[-1, df.columns.get_loc("STOCHk_14_3_1")], 0),
                    "stockd": round(df.iloc[-1, df.columns.get_loc("STOCHd_14_3_1")], 0),
                }

                
                # print(data)
                        
                headers = {
                    "Content-Type": "application/json",
                    "accept": "application/json"
                }
                        #     # requests.post("http://nextjs:3000/api/baro/newBaro", data=data)
                        #     # requests.post("http://10.20.12.164:8000/api/v1/baro/",
                        #     #               json=data1, headers=headers)

                        #     # print(data1Test)
                requests.post(os.environ.get('API') + "v2/alert/",
                                json=data, headers=headers)
                # candle_alert(data=data)
                result = databases.create_document(
                collection_id=os.environ.get('APPWRITE_ALERTID'),
                database_id=os.environ.get('APPWRITE_DATABASEID'),
                document_id="unique()",
                data=data
                )
                return result
    except TypeError as error:
        print({'typeError':error})
    except KeyError as error:
        print({'keyError':error})
    except ValueError as error:
        print({'ValueError':error})
    except AttributeError as error:
        print({'AttributeError':error})

@app.task
def volume_24h_check(baseAsset,quoteAsset):
    '''volume 24h check'''
    ticker = r.get(baseAsset+quoteAsset)
    if ticker is None:
        return 0
    ticker = dict(json.loads(ticker))
    if quoteAsset == 'BTC':
        return float(ticker['q'])

@app.task
def trend_24h_check(baseAsset,quoteAsset):
    ticker = r.get(baseAsset+quoteAsset)
    if ticker is None:
        return 'no data'
    ticker = dict(json.loads(ticker))
    perc = round((float(ticker['c']) * 100 ) / float(ticker['o']) - 100, 2)
    if ticker['o'] > ticker['c']:
        return 'down ' + str(perc) + '%'
    else:
        return 'up ' + str(perc) + '%'
    
