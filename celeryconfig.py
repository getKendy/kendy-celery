broker_url = 'redis://localhost:6379/0'
result_backend = 'redis://localhost:6379/1'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Europe/Amsterdam'
enable_utc = True
include = ['src.binance_tasks','src.barometer_tasks','src.candle_alerts_tasks']
