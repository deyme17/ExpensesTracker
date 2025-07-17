from .mono_webhook_service import MonoWebHookService
from server.services.crud import transaction_service, account_service
from server.services import account_sync_service

mono_webhook_service = MonoWebHookService(transaction_service, account_service, account_sync_service)