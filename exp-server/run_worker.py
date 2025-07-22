from celery_app.config import create_celery
from app.app import create_app
import os

flask_app = create_app()
celery_app = create_celery()
celery_app.conf.update(flask_app.config)

celery_app.autodiscover_tasks(
    ["app.tasks"],
    related_name='tasks'
)

if __name__ == "__main__":
    worker_options = {
        "loglevel": "info",
        "pool": "solo",
        "hostname": f"worker@{os.getenv('COMPUTERNAME', 'localhost')}"
    }
    celery_app.worker_main(argv=["worker"] + [f"--{k}={v}" for k, v in worker_options.items()])