from app.views.screens.splash_screen import SplashScreen
from app.views.screens.first_screen import FirstScreen
from app.views.screens.login_screen import LoginScreen
from app.views.screens.register_screen import RegistrationScreen
from app.views.screens.transactions_screen import TransactionsScreen
from app.views.screens.analytics_screen import AnalyticsScreen

from app.controllers import AnalyticsController, AuthController, TransactionController
    
from app.services import LocalStorageService, AuthService, TransactionProcessor
from app.services.analytics import AnalyticsService
from app.services.crud_services import AccountService, CategoryService, CurrencyService, TransactionService

from app.app import ExpensesTrackerApp


def create_app():
    storage_service = LocalStorageService()
    auth_service = AuthService(storage_service)
    current_user = auth_service.get_current_user()

    account_service = AccountService(
        storage_service=storage_service,
        user_id=current_user.user_id if current_user else None
    )
    category_service = CategoryService(storage_service=storage_service)
    currency_service = CurrencyService(storage_service=storage_service)

    transaction_service = TransactionService(
        user_id=current_user.user_id if current_user else None,
        storage_service=storage_service
    )
    transaction_processor = TransactionProcessor()
    analytics_service = AnalyticsService(category_service)

    auth_controller = AuthController(auth_service)
    transaction_controller = TransactionController(transaction_service, transaction_processor, category_service, currency_service)
    analytics_controller = AnalyticsController(analytics_service)

    return ExpensesTrackerApp(
        storage_service=storage_service,
        auth_controller=auth_controller,
        transaction_controller=transaction_controller,
        analytics_controller=analytics_controller,
        account_service=account_service,
        category_service=category_service,
        currency_service=currency_service,
        splash_screen_cls=SplashScreen,
        first_screen_cls=FirstScreen,
        login_screen_cls=LoginScreen,
        register_screen_cls=lambda name: RegistrationScreen(name=name),
        transactions_screen_cls=TransactionsScreen,
        analytics_screen_cls=AnalyticsScreen,
    )