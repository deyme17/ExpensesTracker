from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import get_color_from_hex

from app.utils.constants import APP_TITLE
from app.utils.theme import BACKGROUND_COLOR


class ExpensesTrackerApp(App):
    def __init__(self, 
                 storage_service, 
                 monobank_service, 
                 auth_controller, 
                 transaction_controller, 
                 analytics_controller, 
                 splash_screen_cls, 
                 first_screen_cls, 
                 login_screen_cls, 
                 register_screen_cls, 
                 transactions_screen_cls, 
                 analytics_screen_cls,
                 **kwargs):
        
        super().__init__(**kwargs)
        self.storage_service = storage_service
        self.monobank_service = monobank_service
        self.auth_controller = auth_controller
        self.transaction_controller = transaction_controller
        self.analytics_controller = analytics_controller

        # screen classes
        self.splash_screen_cls = splash_screen_cls
        self.first_screen_cls = first_screen_cls
        self.login_screen_cls = login_screen_cls
        self.register_screen_cls = register_screen_cls
        self.transactions_screen_cls = transactions_screen_cls
        self.analytics_screen_cls = analytics_screen_cls

        self.screen_manager = ScreenManager()

    def build(self):
        self.title = APP_TITLE
        Window.clearcolor = get_color_from_hex(BACKGROUND_COLOR)
        Window.size = (360, 640)
        
        self._add_screens()
        
        return self.screen_manager
    
    def _add_screens(self):
        # create instances of screens
        splash_screen = self.splash_screen_cls(name='splash_screen')
        first_screen = self.first_screen_cls(name='first_screen')
        login_screen = self.login_screen_cls(
            name='login_screen',
            controller=self.auth_controller
        )
        register_screen = self.register_screen_cls(
            name='reg_screen',
            controller=self.auth_controller
        )
        transactions_screen = self.transactions_screen_cls(
            name='transactions_screen',
            controller=self.transaction_controller
        )
        analytics_screen = self.analytics_screen_cls(
            name='analytics',
            controller=self.analytics_controller
        )

        # add screens to screen manager
        self.screen_manager.add_widget(splash_screen)
        self.screen_manager.add_widget(first_screen)
        self.screen_manager.add_widget(login_screen)
        self.screen_manager.add_widget(register_screen)
        self.screen_manager.add_widget(transactions_screen)
        self.screen_manager.add_widget(analytics_screen)

        self.screen_manager.current = 'splash_screen'
    
    def on_start(self):
        from kivy.clock import Clock
        Clock.schedule_once(lambda dt: self._check_auth_status(), 2)
    
    def _check_auth_status(self):
        if self.auth_controller.is_authenticated():
            self.screen_manager.current = 'transactions_screen'
        else:
            self.screen_manager.current = 'first_screen'
    
    def stop(self):
        self.storage_service.close()
        return super().stop()
