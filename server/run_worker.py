from celery.config import create_celery
from app.app import create_app

flask_app = create_app()
celery_app = create_celery()
celery_app.conf.update(flask_app.config)

celery_app.autodiscover_tasks(["app.tasks"])

if __name__ == "__main__":
    celery_app.worker_main(["worker", "--loglevel=info"])