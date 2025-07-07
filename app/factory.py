# screens
from app.views.screens import SplashScreen, FirstScreen, LoginScreen, RegistrationScreen, TransactionsScreen, AnalyticsScreen
# controllers
from app.controllers import AnalyticsController, AuthController, TransactionController, MetaDataController
# services
from app.services import LocalStorageService, AuthService, TransactionProcessor, DataLoader
from app.services.analytics import AnalyticsService
from app.services.crud_services import AccountService, CategoryService, CurrencyService, TransactionService
# app cls
from app.app import ExpensesTrackerApp


def create_app():
    storage = LocalStorageService()
    
    # services
    category_service = CategoryService(storage)
    currency_service = CurrencyService(storage)
    transaction_processor = TransactionProcessor(category_service)
    analytics_service = AnalyticsService(category_service)
    account_service = AccountService(storage_service=storage)
    transaction_service = TransactionService(storage_service=storage)

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
    meta_data_controller = MetaDataController(currency_service, category_service)

    # app
    return ExpensesTrackerApp(  
        splash_screen_cls=lambda name: SplashScreen(name=name, auth_controller=auth_controller, data_loader=data_loader),
        first_screen_cls=FirstScreen,
        login_screen_cls=lambda name: LoginScreen(name=name, auth_controller=auth_controller),
        register_screen_cls=lambda name: RegistrationScreen(name=name, controller=auth_controller),

        transactions_screen_cls=lambda name: TransactionsScreen(
            name=name, 
            transaction_controller=transaction_controller, 
            meta_data_controller=meta_data_controller,
            storage_service=storage,
            logout_callback=auth_controller.logout),

        analytics_screen_cls=lambda name: AnalyticsScreen(
            name=name,
            transaction_controller=transaction_controller,
            analytics_controller=analytics_controller,
            local_storage=storage,
            logout_callback=auth_controller.logout
        ),
        storage_service=storage,
        is_authenticated=auth_controller.is_authenticated
    )
