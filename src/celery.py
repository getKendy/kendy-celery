from celery import Celery
from celery.schedules import crontab
# import socketio
app = Celery('src')
app.config_from_object('celeryconfig')

# sio =socketio.Client()




# @sio.event
# def connect():
#     print('connection established')


# @sio.event
# def candle_alert(data):
#     sio.emit('tickeralert', data)
    
# @sio.event
# def disconnect():
#     print('disconnected from server')

# sio.connect('http://10.20.31.6:3000')





app.conf.update(
    result_expires=30,   # Minutes
)

app.conf.task_routes = {
    "src.candle_alerts_tasks.*": "candlealerts",
    "src.barometer_tasks.*": "barometer",
    "src.binance_tasks.*": "binance",
    "src.kucoin_tasks.*": "kucoin"
}

app.conf.beat_schedule = {
    "start_kucoin_klines_ticker": {
        "task": "src.kucoin_tasks.start_klines_ticker",
        "schedule": crontab(minute="*/15",hour="*"),
        "args": (),
    },
    "start_binance_klines_ticker": {
        "task": "src.binance_tasks.start_klines_ticker",
        "schedule": crontab(minute="*/15",hour="*"),
        "args": (),
    },
    "get_bin_symbols_from_exchangeinfo":{
        "task": "src.binance_tasks.get_symbols_from_exchangeinfo",
        "schedule": crontab(minute="0",hour="*"),
        "args": (),
    },
    "get_ku_symbols_from_exchangeinfo":{
        "task": "src.kucoin_tasks.get_symbols_from_exchangeinfo",
        "schedule": crontab(minute="0",hour="*"),
        "args": (),
    },
    "get_ku_ticker24h":{
        "task": "src.kucoin_tasks.ticker24h",
        "schedule": crontab(minute="*"),
        "args": (),
    },
    "update_barometer": {
        "task": "src.barometer_tasks.update_barometer",
        "schedule": crontab(minute="*"),
        "args": (),
    },
    "clean_old_tickers": {
        "task": "src.binance_tasks.clean_old_tickers",
        "schedule": crontab(minute="*/2"),
        "args": (),
    },
    "build_ku_indicators_from_1m_candles": {
        "task": "src.candle_alerts_tasks.build_indicators_from_candles",
        "schedule": crontab(minute="*"),
        "kwargs": ({"timeframe":"1m","resample_frame":"1T","exchange":"kucoin"}),
    },
    "build_ku_indicators_from_2m_candles": {
        "task": "src.candle_alerts_tasks.build_indicators_from_candles",
        "schedule": crontab(minute="*/2"),
        "kwargs": ({"timeframe":"2m","resample_frame":"2T","exchange":"kucoin"}),
    },
    "build_ku_indicators_from_3m_candles": {
        "task": "src.candle_alerts_tasks.build_indicators_from_candles",
        "schedule": crontab(minute="*/3"),
        "kwargs": ({"timeframe":"3m","resample_frame":"3T","exchange":"kucoin"}),
    },
    "build_ku_indicators_from_5m_candles": {
        "task": "src.candle_alerts_tasks.build_indicators_from_candles",
        "schedule": crontab(minute="*/5"),
        "kwargs": ({"timeframe":"5m","resample_frame":"5T","exchange":"kucoin"}),
    },
    "build_ku_indicators_from_15m_candles": {
        "task": "src.candle_alerts_tasks.build_indicators_from_candles",
        "schedule": crontab(minute="*/15"),
        "kwargs": ({"timeframe":"15m","resample_frame":"15T","exchange":"kucoin"}),
    },
    "build_ku_indicators_from_30m_candles": {
        "task": "src.candle_alerts_tasks.build_indicators_from_candles",
        "schedule": crontab(minute="*/30"),
        "kwargs": ({"timeframe":"30m","resample_frame":"30T","exchange":"kucoin"}),
    },
    "build_ku_indicators_from_60m_candles": {
        "task": "src.candle_alerts_tasks.build_indicators_from_candles",
        "schedule": crontab(minute="0"),
        "kwargs": ({"timeframe":"60m","resample_frame":"60T","exchange":"kucoin"}),
    },
    "build_indicators_from_1m_candles": {
        "task": "src.candle_alerts_tasks.build_indicators_from_candles",
        "schedule": crontab(minute="*"),
        "kwargs": ({"timeframe":"1m","resample_frame":"1T","exchange":"binance"}),
    },
    "build_indicators_from_2m_candles": {
        "task": "src.candle_alerts_tasks.build_indicators_from_candles",
        "schedule": crontab(minute="*/2"),
        "kwargs": ({"timeframe":"2m","resample_frame":"2T","exchange":"binance"}),
    },
    "build_indicators_from_3m_candles": {
        "task": "src.candle_alerts_tasks.build_indicators_from_candles",
        "schedule": crontab(minute="*/3"),
        "kwargs": ({"timeframe":"3m","resample_frame":"3T","exchange":"binance"}),
    },
    "build_indicators_from_5m_candles": {
        "task": "src.candle_alerts_tasks.build_indicators_from_candles",
        "schedule": crontab(minute="*/5"),
        "kwargs": ({"timeframe":"5m","resample_frame":"5T","exchange":"binance"}),
    },
    "clean_old_alerts": {
        "task": "src.binance_tasks.clean_old_alerts",
        "schedule": crontab(minute="*/5"),
        "args": (),
    },
}

if __name__ == '__main__':
    app.start()
