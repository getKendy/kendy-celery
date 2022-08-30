from celery import Celery
from celery.schedules import crontab

app = Celery('src')
app.config_from_object('celeryconfig')


app.conf.update(
    result_expires=30,   # Minutes
)

app.conf.task_routes = {
    "src.candle_alerts_tasks.*": "candlealerts",
    "src.barometer_tasks.*": "barometer",
    "src.binance_tasks.*": "binance"
}

app.conf.beat_schedule = {
    "start_klines_ticker": {
        "task": "src.binance_tasks.start_klines_ticker",
        "schedule": crontab(minute="*/15"),
        "args": (),
    },
    "get_symbols_from_exchangeinfo":{
         "task": "src.binance_tasks.get_symbols_from_exchangeinfo",
        "schedule": crontab(minute="0",hour="*"),
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
    # "build_indicators_from_1m_candles": {
    #     "task": "src.candle_alerts_tasks.build_indicators_from_candles",
    #     "schedule": crontab(minute="*"),
    #     "kwargs": ({"timeframe":"1m","resample_frame":"1T"}),
    # },
    # "build_indicators_from_2m_candles": {
    #     "task": "src.candle_alerts_tasks.build_indicators_from_candles",
    #     "schedule": crontab(minute="*/2"),
    #     "kwargs": ({"timeframe":"2m","resample_frame":"2T"}),
    # },
    # "build_indicators_from_3m_candles": {
    #     "task": "src.candle_alerts_tasks.build_indicators_from_candles",
    #     "schedule": crontab(minute="*/3"),
    #     "kwargs": ({"timeframe":"3m","resample_frame":"3T"}),
    # },
    "build_indicators_from_5m_candles": {
        "task": "src.candle_alerts_tasks.build_indicators_from_candles",
        "schedule": crontab(minute="*/5"),
        "kwargs": ({"timeframe":"5m","resample_frame":"5T"}),
    }
}

if __name__ == '__main__':
    app.start()
