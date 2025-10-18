from celery import Celery
import os

redis_url = os.getenv('REDIS_URL', 'redis://redis:6379/0')

celery = Celery('verityvue', broker=redis_url, backend=redis_url)
celery.conf.task_queues = []
