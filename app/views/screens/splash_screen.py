from kivy.animation import Animation
from kivy.clock import Clock

from kivy.lang import Builder
from app.utils.language_mapper import LanguageMapper as LM

from app.views.screens.base_screen import BaseScreen
from app.utils.constants import APP_NAME
import threading


# Load kv file
Builder.load_file("kv/splash_screen.kv")


class SplashScreen(BaseScreen):
    """
    Splash screen shown when the app is starting.
    
    This screen displays the app logo and name while the app is initializing.
    """
    
    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)
    
    def on_enter(self):
        """Called when the screen enters the view."""
        super(SplashScreen, self).on_enter()
        print("IDS:", self.ids)

        if "logo" in self.ids:
            self.ids.logo.opacity = 1
            self.ids.logo.size_hint = (0.5, 0.5)
            Animation(opacity=1, size_hint=(0.8, 0.8), duration=1.0).start(self.ids.logo)

        if "app_name_label" in self.ids:
            self.ids.app_name_label.opacity = 0
            Clock.schedule_once(lambda dt: Animation(opacity=1, duration=0.8).start(self.ids.app_name_label), 0.5)

        Clock.schedule_once(self._check_auth, 2.0)
    
    def _check_auth(self, dt):
        """
        Check authentication status and navigate to appropriate screen.
        This is a fallback in case the App class doesn"t handle navigation.
        """
        app = self.get_app()

        if hasattr(app, "auth_controller") and app.auth_controller.is_authenticated():
            if hasattr(self.ids, "loading_label"):
                self.ids.loading_label.text = LM.message("loading_data")

            threading.Thread(target=self._load_data_and_proceed).start()
        else:
            self.switch_screen("first_screen", "left")

    def _load_data_and_proceed(self):
        try:
            app = self.get_app()

            app.category_service.get_categories()
            app.currency_service.get_currencies()
            app.account_service.get_accounts()
            app.transaction_controller.get_transactions(force_refresh=True)

            acc_id = app.account_service.storage_service.get_active_account_id()
            if acc_id:
                app.account_service.storage_service.set_active_account(acc_id)

            from kivy.clock import Clock
            Clock.schedule_once(lambda dt: self.switch_screen("transactions_screen", "left"))
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_error_message(
                f"{LM.message('initialization_error')}: {e}"
            ))

    def get_app(self):
        from kivy.app import App
        return App.get_running_app()