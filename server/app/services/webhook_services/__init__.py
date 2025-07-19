from .mono_webhook_service import MonoWebHookService
from app.services.crud import transaction_service, account_service, user_service

mono_webhook_service = MonoWebHookService(transaction_service, account_service, user_service)