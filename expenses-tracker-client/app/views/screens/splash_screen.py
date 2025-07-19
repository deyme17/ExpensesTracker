from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder

from app.utils.language_mapper import LanguageMapper as LM
from app.views.screens.base_screen import BaseScreen

import threading


# Load kv file
Builder.load_file("kv/splash_screen.kv")


class SplashScreen(BaseScreen):
    """
    Splash screen shown when the app is starting.
    Displays app logo and name while the app is initializing.
    """
    def __init__(self, auth_controller, data_loader, **kwargs):
        super().__init__(**kwargs)
        self.auth_controller = auth_controller
        self.data_loader = data_loader
    
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
        This is a fallback in case the App class doesn't handle navigation.
        """
        if self.auth_controller.is_authenticated():
            print("User is authenticated, starting data loading...")
            threading.Thread(target=self._load_data_and_proceed).start()
        else:
            print("User not authenticated, switching to first screen...")
            self.switch_screen("first_screen", "left")

    def _load_data_and_proceed(self):
        """
        Background thread: loading data, and then calls to transition to the screen.
        """
        try:
            user = self.auth_controller.get_current_user()
            self.data_loader.load_data(user, callback=self._on_data_loaded)
        except Exception as e:
            Clock.schedule_once(lambda dt: self.show_error_message(
                f"{LM.message('initialization_error')}: {e}"
            ))
    
    def _on_data_loaded(self):
        """
        Callback after data loaded.
        """
        Clock.schedule_once(lambda dt: self.switch_screen("transactions_screen", "left"))