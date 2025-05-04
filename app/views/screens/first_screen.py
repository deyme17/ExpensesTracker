from kivy.lang import Builder
from kivy.animation import Animation
from kivy.clock import Clock

from app.views.screens.base_screen import BaseScreen

# Load kv file
Builder.load_file('kv/first_screen.kv')


class FirstScreen(BaseScreen):
    """
    First screen shown to users who are not logged in.
    
    This screen provides options to login or register.
    """
    
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
    
    def login_screen(self, *args):
        """Navigate to the login screen."""
        self.switch_screen('login_screen', 'left')
    
    def reg_screen(self, *args):
        """Navigate to the registration screen."""
        self.switch_screen('reg_screen', 'left')
    
    def on_enter(self):
        """Called when the screen enters the view."""
        super(FirstScreen, self).on_enter()
        
        if hasattr(self, 'logo_container'):
            self.logo_container.opacity = 0
            Animation(opacity=1, d=1.0).start(self.logo_container)
        
        if hasattr(self, 'buttons_container'):
            self.buttons_container.opacity = 0
    
            Clock.schedule_once(
                lambda dt: Animation(opacity=1, d=0.8).start(self.buttons_container),
                0.5
            )
    
    def on_leave(self):
        """Called when the screen leaves the view."""
        super(FirstScreen, self).on_leave()
        
        if hasattr(self, 'logo_container'):
            self.logo_container.opacity = 0
        
        if hasattr(self, 'buttons_container'):
            self.buttons_container.opacity = 0