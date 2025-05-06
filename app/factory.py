from app.views.screens.splash_screen import SplashScreen
from app.views.screens.first_screen import FirstScreen
from app.views.screens.login_screen import LoginScreen
from app.views.screens.register_screen import RegistrationScreen
from app.views.screens.transactions_screen import TransactionsScreen
from app.views.screens.analytics_screen import AnalyticsScreen

from app.controllers.auth_controller import AuthController
from app.controllers.transaction_controller import TransactionController
from app.controllers.analytics_controller import AnalyticsController

from app.services.bank_services.monobank_service import MonobankService
from app.services.local_storage import LocalStorageService

from app.app import ExpensesTrackerApp


def create_app():
    storage_service = LocalStorageService()
    monobank_service = MonobankService()

    auth_controller = AuthController(storage_service)
    transaction_controller = TransactionController(storage_service)
    analytics_controller = AnalyticsController()

    return ExpensesTrackerApp(
        storage_service=storage_service,
        monobank_service=monobank_service,
        auth_controller=auth_controller,
        transaction_controller=transaction_controller,
        analytics_controller=analytics_controller,
        splash_screen_cls=SplashScreen,
        first_screen_cls=FirstScreen,
        login_screen_cls=LoginScreen,
        register_screen_cls=RegistrationScreen,
        transactions_screen_cls=TransactionsScreen,
        analytics_screen_cls=AnalyticsScreen,
    )
