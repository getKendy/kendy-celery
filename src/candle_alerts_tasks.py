from .celery import app
import pandas as pd
import pandas_ta as ta
import redis
import os
import requests
import json

r = redis.Redis(host=os.environ.get('REDIS_CACHE'),
                port=os.environ.get('REDIS_PORT'),
                db=os.environ.get('REDIS_DB'))

@app.task
def build_indicators_from_candles():
    '''build indicators from candles'''
    # dateNow = datetime.datetime.now()
    # queryTime = datetime.datetime.now() - datetime.timedelta(minutes=30)
    # tableTickers = Tickers.objects.all().filter(date__gte=queryTime)
    # tableTickers = indicatorTickers([queryTime, dateNow])

    print('starting calculations')
    keys = r.keys("market*")
    for key in keys:
        # only btc pairs for now!!
        market = dict(json.loads(r.get(key)))
        if market["quoteAsset"] != "BTC":
            continue
        response = requests.get(
            os.environ.get('API') + 'v2/tickers/' + market["symbol"])
        # print(response)
        if not response:
            continue
        filterTicker = response.json()
        print(len(filterTicker))

        if len(filterTicker) > 21:  # minimum 20 tickers to build BolingerBands
            volume_24h = volume_24h_check(baseAsset=market['baseAsset'],quoteAsset=market["quoteAsset"])
            print({'24hVolume':volume_24h})
            if  volume_24h > 50:
                process_ticker_data(ticker_data=filterTicker,volume_24h=volume_24h)

@app.task
def process_ticker_data(ticker_data,volume_24h):
    try:
        # print(df)
        # print(len(filterTicker))
        last_ticker = ticker_data[-1]
        # print(lastTicker)
        # print(type(lastTicker))
        
        if last_ticker['quote'] > 150:       # ! min volume > 150 BTC   
            # print('VOLUME OK')
            # print('creating dataframe')
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
            # print(df.tail())
            # print('creating DateTime')
            df['DateTime'] = pd.to_datetime(df['date'])
            # print('creating index')
            df = df.set_index('DateTime')
            # print('dropping date')
            df = df.drop(['date'], axis=1)
            # !!!! RESAMPLE TICKERS INTO USABLE TIMEFRAMES
            df = df.resample('1T', label='right', closed='right').agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'last',
                'quote': 'last'
            })

            # print(type(lastTicker))
            # print(lastTicker.quote)
            # df = filterTicker.to_timeseries(index="date")
            # print(df.tail())
            # print(len(filterTicker))
            # print(lastTicker)
            # df.ta.indicators()
            # help(ta.bbands)
            # Returns:   BB          > help(ta.bbands)
            #    pd.DataFrame: lower, mid, upper, bandwidth columns.


            df.ta.bbands(
                close=df["close"],
                length=20,
                std=2,
                mamode="sma",
                cumulative=True,
                append=True,
            )
            # print(df.tail(n=20))
            # print(df.columns)
            
            if (
                float(df.iloc[-1, df.columns.get_loc("close")])
                < float(df.iloc[-1, df.columns.get_loc("BBL_20_2.0")])
                and float(df.iloc[-1, df.columns.get_loc("BBB_20_2.0")]) >= 0.5    # min % BB width
            ):
            
                # print(df["BBB_20_2.0"])
                # print(df.iloc[
                #         -1, df.columns.get_loc("symbol", "BBL_20_2.0", "BBL_20_2.0")
                #     ])
                # print(df.tail())
                # Returns:   STOCH       > help(ta.stoch)
                #     pd.DataFrame: %K, %D columns.
                df.ta.stoch(
                    high=df["high"],
                    low=df["low"],
                    smooth_k=1,
                    cumulative=True,
                    append=True,
                )
                # print(df.tail(n=20))
                # print(df.columns)
                # Index(['id', 'symbol', 'market', 'close', 'open', 'high', 'low', 'volume',
                # 'quote', 'BBL_20_2.0', 'BBM_20_2.0', 'BBU_20_2.0', 'BBB_20_2.0',
                # 'STOCHk_14_3_1', 'STOCHd_14_3_1'],dtype='object')
                # df.iloc[-1:]
                
                if float(df.iloc[-1, df.columns.get_loc("STOCHk_14_3_1")]) < 20:
                    print(df.tail(n=20))
                    
                    data = {
                        "date": last_ticker['date'],
                        "symbol": last_ticker['symbol'],
                        "market": last_ticker['market'],
                        "close": round(
                            df.iloc[-1, df.columns.get_loc("close")], 8
                        ),
                        "volume": round(
                            df.iloc[-1, df.columns.get_loc("volume")], 2
                        ),
                        "quote": round(
                            df.iloc[-1, df.columns.get_loc("quote")], 2
                        ),
                        "volume24h": round(volume_24h,2),
                        "bbl": round(
                            df.iloc[-1,
                                    df.columns.get_loc("BBL_20_2.0")], 8
                        ),
                        "bbm": round(
                            df.iloc[-1,
                                    df.columns.get_loc("BBM_20_2.0")], 8
                        ),
                        "bbu": round(
                            df.iloc[-1,
                                    df.columns.get_loc("BBU_20_2.0")], 8
                        ),
                        "bbb": round(
                            df.iloc[-1,
                                    df.columns.get_loc("BBB_20_2.0")], 1
                        ),
                        "stochk": round(
                            df.iloc[-1,
                                    df.columns.get_loc("STOCHk_14_3_1")], 0
                        ),
                        "stockd": round(
                            df.iloc[-1,
                                    df.columns.get_loc("STOCHd_14_3_1")], 0
                        ),
                    }

                    # oldAlerts = r.get("alerts")
                    # # print(oldAlerts)
                    # # print(type(oldAlerts))
                    # if oldAlerts is not None:
                    #     oldAlerts = json.loads(oldAlerts)
                    #     print(type(oldAlerts))
                    #     oldAlerts.append(data)
                    #     r.set("alerts", json.dumps(oldAlerts))
                    # else:
                    #     r.set("alerts", json.dumps([data]))
                    # print('!! ALERT !!')
                    # print('!! ALERT !!')
                    # print('!! ALERT !!')
                    # print(
                    #     {"symbol": df.iloc[-1, df.columns.get_loc("symbol")], })
                    # print('!! ALERT !!')
                    # print('!! ALERT !!')
                    # print('!! ALERT !!')
                    print(data)
                            
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
                    # insertAlert(data)
                    # else:
                    # print('found nothing: '+ lastTicker.date.strftime('%y-%m-%d %H:%M') + '(UTC)  Price: ' +
                    # str(df.iloc[-1, df.columns.get_loc('close')])  +
                    # str(df.iloc[-1, df.columns.get_loc('symbol')]) + ' -> BB: ' +
                    # str(df.iloc[-1, df.columns.get_loc('BBL_20_2.0')]) + ' Stoch: ' +
                    # str(df.iloc[-1, df.columns.get_loc('STOCHk_14_3_1')]))
    except TypeError as error:
        print({'typeError':error})
    except KeyError as error:
        print({'keyError':error})
    except ValueError as error:
        print({'ValueError':error})
        

@app.task
def volume_24h_check(baseAsset,quoteAsset):
    ticker = r.get(baseAsset+quoteAsset)
    if ticker is None:
        return 0
    ticker = dict(json.loads(ticker))
    if quoteAsset == 'BTC':
        return float(ticker['q'])
    