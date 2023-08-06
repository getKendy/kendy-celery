from .celery import app

import redis
import os
import requests
import json
from .fastapi import get_fastapi_token

r = redis.Redis(host=os.environ.get('REDIS_CACHE'),
                port=os.environ.get('REDIS_PORT'),
                db=os.environ.get('REDIS_DBBINANCE'),
                password=os.environ.get('REDIS_PASSWORD'))

from appwrite.client import Client
from appwrite.services.databases import Databases
from appwrite.services.functions import Functions

client = Client()
(client
  .set_endpoint(os.environ.get('APPWITE_ENDPOINT')) # Your API Endpoint
  .set_project(os.environ.get('APPWRITE_PROJECTID')) # Your project ID
  .set_key(os.environ.get('APPWRITE_KEY')) # Your secret API key
)
databases = Databases(client)
functions = Functions(client)

@app.task
def update_barometer(save=False):
    '''update barometer'''
    # if save:
    #     storeTickersToDatabase.delay()
    # try:
    # print(get_connection())
    # dateNow = datetime.datetime.now()
    # brl_markets = []
    # bkrw_markets = []
    # aud_markets = []
    # doge_markets = []
    # eur_markets = []
    # busd_markets = []
    # usdc_markets = []
    # rub_markets = []
    # usdp_markets = []
    # gbp_markets = []
    # trx_markets = []
    # zar_markets = []
    # bidr_markets = []
    # usds_markets = []
    # try_markets = []
    # ngn_markets = []
    # xrp_markets = []
    # uah_markets = []
    # bvnd_markets = []
    # gyen_markets = []
    # ust_markets = []
    # pax_markets = []
    # idrt_markets = []
    # dot_markets = []
    # vai_markets = []
    # dai_markets = []
    # usdt_markets = []
    # tusd_markets = []
    btc_markets = []
    eth_markets = []
    bnb_markets = []
    fiat_btc_markets = []
    fiat_eth_markets = []
    fiat_bnb_markets = []

    keys = r.keys("marketBin*")
    quotePairs = []
    basePairs = ['BRL', 'BKRW', 'AUD', 'DOGE', 'EUR', 'BNB', 'BUSD', 'USDC', 'RUB', 'USDP', 'GBP', 'TRX', 'ZAR', 'BIDR', 'USDS',
                 'TRY', 'NGN', 'XRP', 'UAH', 'BVND', 'GYEN', 'ETH', 'UST', 'PAX', 'IDRT', 'DOT', 'VAI', 'DAI', 'BTC', 'USDT', 'TUSD']
    newPairs = []
    for key in keys:
        market = dict(json.loads(r.get(key)))
        # print(market)
        quotePairs.append(market["quoteAsset"])

        # print(market)
        # print(type(market))
        # if market["quote"] == "BRL":
        #     brl_markets.append(market)
        # if market["quote"] == "BKRW":
        #     bkrw_markets.append(market)
        # if market["quote"] == "AUD":
        #     aud_markets.append(market)
        # if market["quote"] == "DOGE":
        #     doge_markets.append(market)
        # if market["quote"] == "EUR":
        #     eur_markets.append(market)

        # if market["quote"] == "RUB":
        #     rub_markets.append(market)
        # if market["quote"] == "USDP":
        #     usdp_markets.append(market)
        # if market["quote"] == "GBP":
        #     gbp_markets.append(market)
        # if market["quote"] == "TRX":
        #     trx_markets.append(market)
        # if market["quote"] == "ZAR":
        #     zar_markets.append(market)
        # if market["quote"] == "BIDR":
        #     bidr_markets.append(market)
        # if market["quote"] == "USDS":
        #     usds_markets.append(market)
        # if market["quote"] == "TRY":
        #     try_markets.append(market)
        # if market["quote"] == "NGN":
        #     ngn_markets.append(market)
        # if market["quote"] == "XRP":
        #     xrp_markets.append(market)
        # if market["quote"] == "UAH":
        #     uah_markets.append(market)
        # if market["quote"] == "BVND":
        #     bvnd_markets.append(market)
        # if market["quote"] == "GYEN":
        #     gyen_markets.append(market)

        # if market["quote"] == "UST":
        #     ust_markets.append(market)
        # if market["quote"] == "PAX":
        #     pax_markets.append(market)
        # if market["quote"] == "IDRT":
        #     idrt_markets.append(market)
        # if market["quote"] == "DOT":
        #     dot_markets.append(market)
        # if market["quote"] == "VAI":
        #     vai_markets.append(market)
        # if market["quote"] == "DAI":
        #     dai_markets.append(market)
        if market["quoteAsset"] == "BTC":
            btc_markets.append(market)
        if market["quoteAsset"] == "BNB":
            bnb_markets.append(market)
        if market["quoteAsset"] == "ETH":
            eth_markets.append(market)
        if market["quoteAsset"] == "USDT":
            if market["baseAsset"] == "BTC":
                fiat_btc_markets.append(market)
            elif market["baseAsset"] == "ETH":
                fiat_eth_markets.append(market)
            elif market["baseAsset"] == "BNB":
                fiat_bnb_markets.append(market)
            else:
                pass
                # usdt_markets.append(market)

        if market["quoteAsset"] == "TUSD":
            if market["baseAsset"] == "BTC":
                fiat_btc_markets.append(market)
            elif market["baseAsset"] == "ETH":
                fiat_eth_markets.append(market)
            elif market["baseAsset"] == "BNB":
                fiat_bnb_markets.append(market)
            else:
                pass
                # tusd_markets.append(market)

        if market["quoteAsset"] == "USDC":
            if market["baseAsset"] == "BTC":
                fiat_btc_markets.append(market)
            elif market["baseAsset"] == "ETH":
                fiat_eth_markets.append(market)
            elif market["baseAsset"] == "BNB":
                fiat_bnb_markets.append(market)
            else:
                pass
                # usdc_markets.append(market)

        if market["quoteAsset"] == "BUSD":
            if market["baseAsset"] == "BTC":
                fiat_btc_markets.append(market)
            elif market["baseAsset"] == "ETH":
                fiat_eth_markets.append(market)
            elif market["baseAsset"] == "BNB":
                fiat_bnb_markets.append(market)
            else:
                pass
                # busd_markets.append(market)

    quotePairsUnique = list(set(quotePairs))
    # print(quotePairsUnique)
    for pair in quotePairsUnique:
        if pair not in basePairs:
            # print(pair)
            newPairs.append(pair)
    # total_brl_alt_volume = 0.0
    # total_bkrw_alt_volume = 0.0
    # total_aud_alt_volume = 0.0
    # total_doge_alt_volume = 0.0
    # total_rub_alt_volume = 0.0
    # total_trx_alt_volume = 0.0
    # total_zar_alt_volume = 0.0
    # total_bidr_alt_volume = 0.0
    # total_try_alt_volume = 0.0
    # total_ngn_alt_volume = 0.0
    # total_xrp_alt_volume = 0.0
    # total_bvnd_alt_volume = 0.0
    # total_gyen_alt_volume = 0.0
    # total_idrt_alt_volume = 0.0
    # total_dot_alt_volume = 0.0
    # total_vai_alt_volume = 0.0
    # total_dai_alt_volume = 0.0
    # total_pax_alt_volume = 0.0
    # total_usds_alt_volume = 0.0
    # total_uah_alt_volume = 0.0
    # total_ust_alt_volume = 0.0
    # total_eur_alt_volume = 0.0
    # total_busd_alt_volume = 0.0
    # total_usdc_alt_volume = 0.0
    # total_usdp_alt_volume = 0.0
    # total_gbp_alt_volume = 0.0
    # total_usdt_alt_volume = 0.0
    # total_tusd_alt_volume = 0.0

    total_btc_alt_volume = 0.0
    total_eth_alt_volume = 0.0
    total_bnb_alt_volume = 0.0
    total_btc_fiat_volume = 0.0
    total_eth_fiat_volume = 0.0
    total_bnb_fiat_volume = 0.0

    # for market in brl_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_brl_alt_volume += float(ticker["q"])
    # for market in bkrw_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_bkrw_alt_volume += float(ticker["q"])
    # for market in aud_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_aud_alt_volume += float(ticker["q"])
    # for market in doge_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_doge_alt_volume += float(ticker["q"])
    # for market in eur_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_eur_alt_volume += float(ticker["q"])

    # for market in busd_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_busd_alt_volume += float(ticker["q"])
    # for market in usdc_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_usdc_alt_volume += float(ticker["q"])
    # for market in rub_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_rub_alt_volume += float(ticker["q"])
    # for market in usdp_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_usdp_alt_volume += float(ticker["q"])
    # for market in gbp_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_gbp_alt_volume += float(ticker["q"])
    # for market in trx_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_trx_alt_volume += float(ticker["q"])
    # for market in zar_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_zar_alt_volume += float(ticker["q"])
    # for market in bidr_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_bidr_alt_volume += float(ticker["q"])
    # for market in usds_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_usds_alt_volume += float(ticker["q"])
    # for market in try_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_try_alt_volume += float(ticker["q"])
    # for market in ngn_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_ngn_alt_volume += float(ticker["q"])
    # for market in xrp_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_xrp_alt_volume += float(ticker["q"])
    # for market in uah_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_uah_alt_volume += float(ticker["q"])
    # for market in bvnd_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_bvnd_alt_volume += float(ticker["q"])
    # for market in gyen_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_gyen_alt_volume += float(ticker["q"])

    # for market in ust_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_ust_alt_volume += float(ticker["q"])
    # for market in pax_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_pax_alt_volume += float(ticker["q"])
    # for market in idrt_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_idrt_alt_volume += float(ticker["q"])
    # for market in dot_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_dot_alt_volume += float(ticker["q"])
    # for market in vai_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_vai_alt_volume += float(ticker["q"])
    # for market in dai_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_dai_alt_volume += float(ticker["q"])

    # for market in usdt_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_usdt_alt_volume += float(ticker["q"])
    # for market in tusd_markets:
    #     ticker = r.get(market["id"])
    #     if ticker is not None:
    #         ticker = dict(json.loads(ticker))
    #         total_tusd_alt_volume += float(ticker["q"])
####
    for market in btc_markets:
        ticker = r.get(market["symbol"])
        if ticker is not None:
            ticker = dict(json.loads(ticker))
            total_btc_alt_volume += float(ticker["q"])  # volume = BTC

    for market in eth_markets:
        ticker = r.get(market["symbol"])
        if ticker is not None:
            ticker = dict(json.loads(ticker))
            total_eth_alt_volume += float(ticker["q"])  # voluem = ETH

    for market in bnb_markets:
        ticker = r.get(market["symbol"])
        if ticker is not None:
            ticker = dict(json.loads(ticker))
            total_bnb_alt_volume += float(ticker["q"])  # volume = BNB

    for market in fiat_btc_markets:
        ticker = r.get(market["symbol"])
        if ticker is not None:
            ticker = dict(json.loads(ticker))
            total_btc_fiat_volume += float(ticker["q"])  # volume = USD

    for market in fiat_eth_markets:
        ticker = r.get(market["symbol"])
        if ticker is not None:
            ticker = dict(json.loads(ticker))
            total_eth_fiat_volume += float(ticker["q"])  # volume = USD

    for market in fiat_bnb_markets:
        ticker = r.get(market["symbol"])
        if ticker is not None:
            ticker = dict(json.loads(ticker))
            total_bnb_fiat_volume += float(ticker["q"])  # volume = USD

    # total_brl_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="BRL") * total_brl_alt_volume, 2)
    # total_bkrw_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="BKRW") * total_bkrw_alt_volume, 2)
    # total_aud_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="AUD") * total_aud_alt_volume, 2)
    # total_doge_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="DOGE") * total_doge_alt_volume, 2)
    # total_rub_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="RUB") * total_rub_alt_volume, 2)
    # total_trx_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="TRX") * total_trx_alt_volume, 2)
    # total_zar_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="ZAR") * total_zar_alt_volume, 2)
    # total_bidr_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="BIDR") * total_bidr_alt_volume, 2)
    # total_try_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="TRY") * total_try_alt_volume, 2)
    # total_ngn_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="NGN") * total_ngn_alt_volume, 2)
    # total_xrp_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="XRP") * total_xrp_alt_volume, 2)
    # total_bvnd_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="BVND") * total_bvnd_alt_volume, 2)
    # total_gyen_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="GYEN") * total_gyen_alt_volume, 2)
    # total_idrt_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="IDRT") * total_idrt_alt_volume, 2)
    # total_dot_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="DOT") * total_dot_alt_volume, 2)
    # total_vai_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="VAI") * total_vai_alt_volume, 2)
    # total_dai_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="DAI") * total_dai_alt_volume, 2)
    # total_pax_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="PAX") * total_pax_alt_volume, 2)
    # total_usds_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="USDS") * total_usds_alt_volume, 2)
    # total_uah_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="UAH") * total_uah_alt_volume, 2)
    # total_ust_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="UST") * total_ust_alt_volume, 2)
    # total_eur_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="EUR") * total_eur_alt_volume, 2)
    # total_busd_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="BUSD") * total_busd_alt_volume, 2)
    # total_usdc_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="USDC") * total_usdc_alt_volume, 2)
    # total_usdp_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="USDP") * total_usdp_alt_volume, 2)
    # total_gbp_alt_volume_usdt = round(
    #     calculate_dollar_price(coin="GBP") * total_gbp_alt_volume, 2)

    total_btc_alt_volume_usdt = round(
        calculate_dollar_price(coin="BTC") * total_btc_alt_volume, 2
    )
    total_bnb_alt_volume_usdt = round(
        calculate_dollar_price(coin="ETH") * total_eth_alt_volume, 2
    )
    total_eth_alt_volume_usdt = round(
        calculate_dollar_price(coin="BNB") * total_bnb_alt_volume, 2
    )
    # print(functions.create_execution('calculate_dollar_price','BTC'))
    # print(float(functions.create_execution('calculate_dollar_price','BTC')['response']))
    # print(type(functions.create_execution('calculate_dollar_price','BTC')['response']))
    # total_btc_alt_volume_usdt= round(float(functions.create_execution('calculate_dollar_price','BTC')['response']) * total_btc_alt_volume, 2)
    # total_bnb_alt_volume_usdt= round(float(functions.create_execution('calculate_dollar_price','ETH')['response']) * total_eth_alt_volume, 2)
    # total_eth_alt_volume_usdt= round(float(functions.create_execution('calculate_dollar_price','BNB')['response']) * total_bnb_alt_volume, 2)

    total_volume = (
        total_btc_alt_volume_usdt
        + total_eth_alt_volume_usdt
        + total_bnb_alt_volume_usdt
        + total_btc_fiat_volume
        + total_eth_fiat_volume
        + total_bnb_fiat_volume
        # + total_brl_alt_volume_usdt
        # + total_bkrw_alt_volume_usdt
        # + total_aud_alt_volume_usdt
        # + total_doge_alt_volume_usdt
        # + total_rub_alt_volume_usdt/
        # + total_trx_alt_volume_usdt
        # + total_zar_alt_volume_usdt
        # + total_bidr_alt_volume_usdt
        # + total_try_alt_volume_usdt
        # + total_ngn_alt_volume_usdt
        # + total_xrp_alt_volume_usdt
        # + total_bvnd_alt_volume_usdt
        # + total_gyen_alt_volume_usdt
        # + total_idrt_alt_volume_usdt
        # + total_dot_alt_volume_usdt
        # + total_vai_alt_volume_usdt
        # + total_dai_alt_volume_usdt
        # + total_pax_alt_volume_usdt
        # + total_usds_alt_volume_usdt
        # + total_uah_alt_volume_usdt
        # + total_ust_alt_volume_usdt
        # + total_eur_alt_volume_usdt
        # + total_busd_alt_volume_usdt
        # + total_usdc_alt_volume_usdt
        # + total_usdp_alt_volume_usdt
        # + total_gbp_alt_volume_usdt
    )

    try:
        btc_strength = round(
            (total_btc_fiat_volume * 100)
            / total_volume,
            4,
        )
    except TypeError:
        btc_strength = 0
    except ZeroDivisionError:
        btc_strength = 0

    try:
        eth_strength = round(
            (total_eth_fiat_volume * 100)
            / total_volume,
            4,
        )
    except TypeError:
        eth_strength = 0
    except ZeroDivisionError:
        eth_strength = 0

    try:
        bnb_strength = round(
            (total_bnb_fiat_volume * 100)
            / total_volume,
            4,
        )
    except TypeError:
        bnb_strength = 0
    except ZeroDivisionError:
        bnb_strength = 0

    try:
        btc_alt_strength = round(
            (total_btc_alt_volume_usdt * 100)
            / total_volume,
            4,
        )
    except TypeError:
        btc_alt_strength = 0
    except ZeroDivisionError:
        btc_alt_strength = 0

    try:
        eth_alt_strength = round(
            (total_eth_alt_volume_usdt * 100)
            / total_volume,
            4,
        )
    except TypeError:
        eth_alt_strength = 0
    except ZeroDivisionError:
        eth_alt_strength = 0

    try:
        bnb_alt_strength = round(
            (total_bnb_alt_volume_usdt * 100)
            / total_volume,
            4,
        )
    except TypeError:
        bnb_alt_strength = 0
    except ZeroDivisionError:
        bnb_alt_strength = 0

#     # data = [
#     #     dateNow,
#     #     total_btc_fiat_volume,
#     #     total_eth_fiat_volume,
#     #     total_bnb_fiat_volume,
#     #     total_btc_alt_volume_usdt,
#     #     total_eth_alt_volume_usdt,
#     #     total_bnb_alt_volume_usdt,
#     #     total_volume,
#     #     btc_strength,
#     #     eth_strength,
#     #     bnb_strength,
#     # ]
#     data = {

#         "fiatBtcVolume": total_btc_fiat_volume,
#         "fiatEthVolume": total_eth_fiat_volume,
#         "fiatBnbVolume": total_bnb_fiat_volume,
#         "btcAltVolume": total_btc_alt_volume_usdt,
#         "ethAltVolume": total_eth_alt_volume_usdt,
#         "bnbAltVolume": total_bnb_alt_volume_usdt,
#         "totalVolume": total_volume,
#         "altBtcStrength": btc_strength,
#         "altEthStrength": eth_strength,
#         "altBnbStrength": bnb_strength,
#     }
    data = {
        # "date": datetime.datetime.now().strftime("%s"),
        "fiatBtcVolume": (total_btc_fiat_volume / 1000000),
        "fiatEthVolume": (total_eth_fiat_volume / 1000000),
        "fiatBnbVolume": (total_bnb_fiat_volume / 1000000),
        "btcAltVolume": (total_btc_alt_volume_usdt / 1000000),
        "ethAltVolume": (total_eth_alt_volume_usdt / 1000000),
        "bnbAltVolume": (total_bnb_alt_volume_usdt / 1000000),
        "totalVolume": (total_volume / 1000000),
        "btcStrength": btc_strength,
        "ethStrength": eth_strength,
        "bnbStrength": bnb_strength,
        "altBtcStrength": btc_alt_strength,
        "altEthStrength": eth_alt_strength,
        "altBnbStrength": bnb_alt_strength,
        # "total_brl_alt_volume_usdt": (total_brl_alt_volume_usdt / 1000000),
        # "total_bkrw_alt_volume_usdt": (total_bkrw_alt_volume_usdt / 1000000),
        # "total_aud_alt_volume_usdt": (total_aud_alt_volume_usdt / 1000000),
        # "total_doge_alt_volume_usdt": (total_doge_alt_volume_usdt / 1000000),
        # "total_rub_alt_volume_usdt": (total_rub_alt_volume_usdt / 1000000),
        # "total_trx_alt_volume_usdt": (total_trx_alt_volume_usdt / 1000000),
        # "total_zar_alt_volume_usdt": (total_zar_alt_volume_usdt / 1000000),
        # "total_bidr_alt_volume_usdt": (total_bidr_alt_volume_usdt / 1000000),
        # "total_try_alt_volume_usdt": (total_try_alt_volume_usdt / 1000000),
        # "total_ngn_alt_volume_usdt": (total_ngn_alt_volume_usdt / 1000000),
        # "total_xrp_alt_volume_usdt": (total_xrp_alt_volume_usdt / 1000000),
        # "total_bvnd_alt_volume_usdt": (total_bvnd_alt_volume_usdt / 1000000),
        # "total_gyen_alt_volume_usdt": (total_gyen_alt_volume_usdt / 1000000),
        # "total_idrt_alt_volume_usdt": (total_idrt_alt_volume_usdt / 1000000),
        # "total_dot_alt_volume_usdt": (total_dot_alt_volume_usdt / 1000000),
        # "total_vai_alt_volume_usdt": (total_vai_alt_volume_usdt / 1000000),
        # "total_dai_alt_volume_usdt": (total_dai_alt_volume_usdt / 1000000),
        # "total_pax_alt_volume_usdt": (total_pax_alt_volume_usdt / 1000000),
        # "total_usds_alt_volume_usdt": (total_usds_alt_volume_usdt / 1000000),
        # "total_uah_alt_volume_usdt": (total_uah_alt_volume_usdt / 1000000),
        # "total_ust_alt_volume_usdt": (total_ust_alt_volume_usdt / 1000000),
        # "total_eur_alt_volume_usdt": (total_eur_alt_volume_usdt / 1000000),
        # "total_busd_alt_volume_usdt": (total_busd_alt_volume_usdt / 1000000),
        # "total_usdc_alt_volume_usdt": (total_usdc_alt_volume_usdt / 1000000),
        # "total_usdp_alt_volume_usdt": (total_usdp_alt_volume_usdt / 1000000),
        # "total_gbp_alt_volume_usdt": (total_gbp_alt_volume_usdt / 1000000),
    }
    
    # print(data)
    
#     # connect(host=MONGO_URL)
#     data1 = {
#         "date": datetime.datetime.now().strftime("%m/%d/%Y, %H:%M"),
#         "fiatBtcVolume": (total_btc_fiat_volume / 1000000),
#         "fiatEthVolume": (total_eth_fiat_volume / 1000000),
#         "fiatBnbVolume": (total_bnb_fiat_volume / 1000000),
#         "btcAltVolume": (total_btc_alt_volume_usdt / 1000000),
#         "ethAltVolume": (total_eth_alt_volume_usdt / 1000000),
#         "bnbAltVolume": (total_bnb_alt_volume_usdt / 1000000),
#         "totalVolume": (total_volume / 1000000),
#         "altBtcStrength": btc_strength,
#         "altEthStrength": eth_strength,
#         "altBnbStrength": bnb_strength,
#     }
    token = get_fastapi_token()
    print(token)
    print(type(token))
    headers = {
        "Authorization": token['token_type'] + " " + token['access_token'],
        "Content-Type": "application/json",
        "accept": "application/json"
    }
#     # requests.post("http://nextjs:3000/api/baro/newBaro", data=data)
#     # requests.post("http://10.20.12.164:8000/api/v1/baro/",
#     #               json=data1, headers=headers)

#     # print(data1Test)
    requests.post(os.environ.get('API') + "v2/baro/",
                  json=data, headers=headers)
    # result = databases.create_document(
    #     collection_id=os.environ.get('APPWRITE_BAROMETERID'),
    #     database_id=os.environ.get('APPWRITE_DATABASEID'),
    #     document_id="unique()",
    #     data=data
    #     )
    return
#     # insertBaroData(baroData=data)
#     # baroTable = Baro(date=dateNow,
#     #                  fiatBtcVolume=total_btc_fiat_volume,
#     #                  fiatEthVolume=total_eth_fiat_volume,
#     #                  fiatBnbVolume=total_bnb_fiat_volume,
#     #                  btcAltVolume=total_btc_alt_volume_usdt,
#     #                  ethAltVolume=total_eth_alt_volume_usdt,
#     #                  bnbAltVolume=total_bnb_alt_volume_usdt,
#     #                  totalVolume=total_volume,
#     #                  altBtcStrength=btc_strength,
#     #                  altEthStrength=eth_strength,
#     #                  altBnbStrength=bnb_strength)
#     # baroTable.save()
#     # disconnect()



@app.task
def calculate_dollar_price(coin):
    '''calculate dollar price'''
    try:
        price = dict(json.loads(r.get(coin + "USDT")))
        # print(price)
        price = float(price["c"])
    except TypeError:
        noValueCoins = ["BCX", "JEX", "QI"]
        if coin not in noValueCoins:
            price = get_database_price_for_pair(coin + "USDT")
            if price == 0:
                price = get_database_price_for_pair("USDT" + coin)
                # print(price)
                if price == 0:
                    return 0
            # print(price)
        else:
            price = 0
    return price



@app.task
def calculate_bitcoin_brice(coin):
    '''calculate bitcoin price'''
    try:
        # print(coin)
        price = dict(json.loads(r.get(coin + "BTC")))
        # print(price)
        price = float(price["c"])
    except TypeError:
        if coin == "BTC":
            price = 1
        else:
            noValueCoins = ["BCX", "JEX", "QI", "SBTC"]
            if coin not in noValueCoins:
                price = get_database_price_for_pair(coin + "BTC")

            else:
                price = 0
    return price


@app.task
def get_database_price_for_pair(pair):
    '''get database price for pair'''
    # print(pair)
    try:
        # connect(host=MONGO_URL)
        token = get_fastapi_token()
        # print(token)
        headers = {
            "Authorization": token['token_type'] + " " + token['access_token'],
            "Content-Type": "application/json",
            "accept": "application/json"
        }
        obj = requests.get(os.environ.get('API') + "v2/ticker/" + pair, headers=headers)
        # obj = Tickers.objects.filter(market=pair).last()
        # obj = filterTickers(market=pair)

        if not obj:

            return 0
        # print(obj)
        # print(obj.json())
        # disconnect()
        data = obj.json()
        # print(data)
        # print(type(data))
        price = data['close']
        # print(price)
        return price
    except AttributeError:
        # print("Att error")
        price = 0
    except IndexError:
        # print("Index error")
        price = 0
    return price
