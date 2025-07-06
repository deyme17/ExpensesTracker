from app.views.screens.splash_screen import SplashScreen
from app.views.screens.first_screen import FirstScreen
from app.views.screens.login_screen import LoginScreen
from app.views.screens.register_screen import RegistrationScreen
from app.views.screens.transactions_screen import TransactionsScreen
from app.views.screens.analytics_screen import AnalyticsScreen

from app.controllers import AnalyticsController, AuthController, TransactionController
    
from app.services import LocalStorageService, AuthService, TransactionProcessor, DataLoader
from app.services.analytics import AnalyticsService
from app.services.crud_services import AccountService, CategoryService, CurrencyService, TransactionService

from app.app import ExpensesTrackerApp


def create_app():
    storage = LocalStorageService()
    
    category_service = CategoryService(storage)
    currency_service = CurrencyService(storage)
    transaction_processor = TransactionProcessor(category_service)
    analytics_service = AnalyticsService(category_service)

    # services
    account_service = AccountService(storage)
    transaction_service = TransactionService(None, storage)

    # DataLoader
    data_loader = DataLoader(
        storage,
        account_service,
        transaction_service, 
        category_service,
        currency_service
    )

    # auth
    auth = AuthService(storage, data_loader, account_service, transaction_service)

    # controllers
    auth_controller = AuthController(auth)
    transaction_controller = TransactionController(
        transaction_service,
        transaction_processor,
        category_service,
        currency_service
    )
    analytics_controller = AnalyticsController(analytics_service)

    return ExpensesTrackerApp(
        storage_service=storage,
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
