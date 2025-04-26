from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.image import Image
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.lang import Builder

from app.views.screens.base_screen import BaseScreen
from app.utils.constants import APP_NAME

# Load kv file
Builder.load_file('kv/splash_screen.kv')


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
        
        if hasattr(self, 'logo_image'):
            self.logo_image.opacity = 0
            self.logo_image.size_hint = (0.5, 0.5)
            
            anim = Animation(
                opacity=1,
                size_hint=(0.8, 0.8),
                duration=1.0
            )
            anim.start(self.logo_image)
        
        if hasattr(self, 'app_name_label'):
            self.app_name_label.opacity = 0
            
            Clock.schedule_once(
                lambda dt: Animation(opacity=1, duration=0.8).start(self.app_name_label),
                0.5
            )

        Clock.schedule_once(self._check_auth, 2.0)
    
    def _check_auth(self, dt):
        """
        Check authentication status and navigate to appropriate screen.
        
        This is a fallback in case the App class doesn't handle navigation.
        """
        app = self.get_app()
        if hasattr(app, 'auth_controller') and app.auth_controller.is_authenticated():
            self.switch_screen('transactions_screen', 'left')
        else:
            self.switch_screen('first_screen', 'left')
    
    def get_app(self):
        """Get the running App instance."""
        from kivy.app import App
        return App.get_running_app()