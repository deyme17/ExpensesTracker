from app.services.webhook_services import webhook_services
from app.database.db import SessionLocal
from celery import shared_task

import logging
logger = logging.getLogger(__name__)


@shared_task
def handle_webhook_task(data, bank_name):
    db = SessionLocal()
    try:
        service = webhook_services.get(bank_name)
        if not service:
            raise ValueError(f"Webhook service not found for bank: {bank_name}")

        service.save_hooked_transactions(data, db)
        db.commit()
        logger.info(f"Successfully processed webhook for {bank_name}")

    except Exception as e:
        db.rollback()
        logger.error(f"Error processing webhook for {bank_name}: {str(e)}")
        raise e
    
    finally:
        db.close()
