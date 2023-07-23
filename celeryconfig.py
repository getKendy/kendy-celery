import os

broker_url = os.environ.get('CELERY_BROKER_URL')
result_backend = os.environ.get('CELERY_RESULT_BACKEN')
# broker_url = 'redis://redis:6379/1'
# result_backend = 'redis://redis:6379/2'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Amsterdam'
enable_utc = True
include = ['src.binance_tasks','src.kucoin_tasks','src.barometer_tasks','src.candle_alerts_tasks']
