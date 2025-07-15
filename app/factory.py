# screens
from app.views.screens import SplashScreen, FirstScreen, LoginScreen, RegistrationScreen, TransactionsScreen, AnalyticsScreen
# controllers
from app.controllers import AnalyticsController, AuthController, TransactionController, MetaDataController, GraphFactory
# services
from app.services import AuthService, TransactionProcessor, DataLoader, AnalyticsService
from app.services.crud_services import AccountService, CategoryService, CurrencyService, TransactionService
# app cls
from app.app import ExpensesTrackerApp
# local db
from app.database.db_manager import LocalDBManager


def create_app():
    local_storage = LocalDBManager()
    
    # services
    category_service = CategoryService(local_storage)
    currency_service = CurrencyService(local_storage)
    transaction_processor = TransactionProcessor(category_service)
    analytics_service = AnalyticsService(category_service)
    account_service = AccountService(local_storage=local_storage, user_id=None)
    transaction_service = TransactionService(local_storage=local_storage, user_id=None)

    # DataLoader
    data_loader = DataLoader(
        local_storage,
        account_service,
        transaction_service, 
        category_service,
        currency_service
    )

    # auth
    auth = AuthService(local_storage, data_loader, account_service, transaction_service)

    # controllers
    auth_controller = AuthController(auth)
    transaction_controller = TransactionController(
        transaction_service,
        transaction_processor,
        category_service,
        currency_service
    )
    graph_factory = GraphFactory(category_service)
    analytics_controller = AnalyticsController(analytics_service)
    meta_data_controller = MetaDataController(currency_service, category_service)

    # CallBack
    def refresh_analytics():
        from kivy.app import App
        app = App.get_running_app()
        analytics_screen = app.root.get_screen("analytics_screen")
        analytics_screen.refresh_analytics()

    # app
    return ExpensesTrackerApp(  
        splash_screen_cls=lambda name: SplashScreen(name=name, auth_controller=auth_controller, data_loader=data_loader),
        first_screen_cls=FirstScreen,
        login_screen_cls=lambda name: LoginScreen(name=name, auth_controller=auth_controller),
        register_screen_cls=lambda name: RegistrationScreen(name=name, auth_controller=auth_controller),

        transactions_screen_cls=lambda name: TransactionsScreen(
            name=name, 
            transactions_controller=transaction_controller, 
            meta_data_controller=meta_data_controller,
            local_storage=local_storage,
            update_analytics_callback=refresh_analytics,
            logout_callback=auth_controller.logout),

        analytics_screen_cls=lambda name: AnalyticsScreen(
            name=name,
            transaction_controller=transaction_controller,
            analytics_controller=analytics_controller,
            graph_factory=graph_factory,
            local_storage=local_storage,
            logout_callback=auth_controller.logout
        ),
        local_storage=local_storage,
        is_authenticated=auth_controller.is_authenticated
    )
