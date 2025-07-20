from celery import Celery
from dotenv import load_dotenv
import os

load_dotenv()
BROKER_URL = os.getenv("BROKER_URL")
if not BROKER_URL:
    raise ValueError("BROKER_URL is not set in environment variables")

def create_celery(task_name: str = "ext_celery") -> Celery:                                  # ext - expenses tracker ^_^
    celery_app = Celery(
        task_name,
        broker=BROKER_URL,
        backend=BROKER_URL,
        include=['app.tasks.webhook_tasks'] 
    )
    celery_app.conf.update(
        task_serializer='json',
        accept_content=['json'],
        result_serializer='json',
        timezone='UTC',
        enable_utc=True,
    )
    return celery_app