from app.services.auth_service import AuthService
from app.services.bank_services.monobank_service import MonobankService
from app.services.bank_sync_service import BankSyncService

from app.services.crud import user_service, account_service, transaction_service, category_service

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