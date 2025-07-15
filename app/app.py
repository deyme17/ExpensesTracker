from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager
from kivy.utils import get_color_from_hex

from app.utils.constants import APP_TITLE
from app.utils.theme import BACKGROUND_COLOR


class ExpensesTrackerApp(App):
    def __init__(self, 
                 splash_screen_cls, 
                 first_screen_cls, 
                 login_screen_cls, 
                 register_screen_cls, 
                 transactions_screen_cls, 
                 analytics_screen_cls,
                 local_storage,
                 is_authenticated,
                 **kwargs):
        super().__init__(**kwargs)
        self.splash_screen_cls = splash_screen_cls
        self.first_screen_cls = first_screen_cls
        self.login_screen_cls = login_screen_cls
        self.register_screen_cls = register_screen_cls
        self.transactions_screen_cls = transactions_screen_cls
        self.analytics_screen_cls = analytics_screen_cls

        self.local_storage = local_storage
        self.is_authenticated = is_authenticated

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
        login_screen = self.login_screen_cls(name='login_screen')
        register_screen = self.register_screen_cls(name='reg_screen')
        transactions_screen = self.transactions_screen_cls(name='transactions_screen')
        analytics_screen = self.analytics_screen_cls(name='analytics_screen')

        # add screens to screen manager
        self.screen_manager.add_widget(splash_screen)
        self.screen_manager.add_widget(first_screen)
        self.screen_manager.add_widget(login_screen)
        self.screen_manager.add_widget(register_screen)
        self.screen_manager.add_widget(transactions_screen)
        self.screen_manager.add_widget(analytics_screen)

        self.screen_manager.current = 'splash_screen'
    
    def _check_auth_status(self):
        if self.is_authenticated():
            self.screen_manager.current = 'transactions_screen'
        else:
            self.screen_manager.current = 'first_screen'
    
    def stop(self):
        self.local_storage.close()
        return super().stop()
