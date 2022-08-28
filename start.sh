docker run -d -p 6379:6379 redis
celery -A src worker --loglevel=INFO -B
celery flower -A src --port=5555