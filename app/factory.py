from app.views.screens.splash_screen import SplashScreen
from app.views.screens.first_screen import FirstScreen
from app.views.screens.login_screen import LoginScreen
from app.views.screens.register_screen import RegistrationScreen
from app.views.screens.transactions_screen import TransactionsScreen
from app.views.screens.analytics_screen import AnalyticsScreen

from app.controllers.auth_controller import AuthController
from app.controllers.transaction_controller import TransactionController
from app.controllers.analytics_controller import AnalyticsController

from app.services.local_storage import LocalStorageService
from app.services.auth_service import AuthService
from app.services.crud_services.transaction import TransactionService
from app.services.crud_services.account import AccountService

from app.app import ExpensesTrackerApp


def create_app():
    storage_service = LocalStorageService()
    auth_service = AuthService(storage_service)
    current_user = auth_service.get_current_user()

    account_service = AccountService(
        storage_service=storage_service,
        user_id=current_user.user_id if current_user else None
    )

    transaction_service = TransactionService(
        user_id=current_user.user_id if current_user else None,
        storage_service=storage_service,
        offline_mode=current_user is None
    )

    auth_controller = AuthController(storage_service)
    transaction_controller = TransactionController(transaction_service)
    analytics_controller = AnalyticsController()

    return ExpensesTrackerApp(
        storage_service=storage_service,
        auth_controller=auth_controller,
        transaction_controller=transaction_controller,
        analytics_controller=analytics_controller,
        account_service=account_service,
        splash_screen_cls=SplashScreen,
        first_screen_cls=FirstScreen,
        login_screen_cls=LoginScreen,
        register_screen_cls=lambda name: RegistrationScreen(name=name),
        transactions_screen_cls=TransactionsScreen,
        analytics_screen_cls=AnalyticsScreen,
    )