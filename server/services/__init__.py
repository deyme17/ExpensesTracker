# Auth
from server.services.auth_service import AuthService
from server.services.bank_services.monobank_service import MonobankService
from server.services.bank_sync_service import BankSyncService

from server.services import user_service, account_service, transaction_service, category_service

bank_sync_service = BankSyncService(
    account_service=account_service,
    transaction_service=transaction_service,
    category_service=category_service
)
auth_service = AuthService(
    user_service=user_service,
    bank_service_cls=MonobankService,
    bank_sync_service=bank_sync_service
)


# WebHook
from .webhook_service import WebHookService

webhook_service = WebHookService()