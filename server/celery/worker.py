from celery.config import create_celery
from app.app import create_app

flask_app = create_app()
celery = create_celery()
celery.conf.update(flask_app.config)

celery.autodiscover_tasks(["app.tasks"])