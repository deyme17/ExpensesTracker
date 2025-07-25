from kivy.properties import StringProperty, NumericProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder

from app.utils.language_mapper import LanguageMapper as LM
from app.views.screens.base_screen import BaseScreen

# Load kv file
Builder.load_file("kv/login_screen.kv")


class LoginScreen(BaseScreen):
    """
    Screen for user login.
    Handles the UI representation of the login process, delegating actual
    authentication logic to the AuthController.
    """
    error_message = StringProperty("")
    show_error = NumericProperty(0)
    
    def __init__(self, auth_controller, **kwargs):
        super(LoginScreen, self).__init__(**kwargs)
        self.auth_controller=auth_controller
    
    def on_enter(self):
        """Reset login button and input fields when screen is entered."""
        super(LoginScreen, self).on_enter()
        self.login_button.text = LM.message("login_button")
        self.login_button.disabled = False
        self.email_input.text = ""
        self.password_input.text = ""
        self.error_message = ""
        self.show_error = 0
    
    def go_back(self):
        """Navigate back to the first screen."""
        self.switch_screen("first_screen", "right")
    
    def go_to_registration(self):
        """Navigate to the registration screen."""
        self.switch_screen("reg_screen", "left")
    
    def login(self):
        """
        Process login attempt.
        
        Validates input fields and delegates authentication to the controller.
        """
        email = self.email_input.text
        password = self.password_input.text
        
        if not email:
            self.error_message = LM.message("enter_email")
            self._show_error()
            return
        
        if not password:
            self.error_message = LM.message("enter_password")
            self._show_error()
            return
        
        self.login_button.text = LM.message("auth_title") + "..."
        self.login_button.disabled = True
        
        def auth_callback(success, message):
            if success:
                self.switch_screen("transactions_screen", "left")
            else:
                self.error_message = message
                self._show_error()
                self.login_button.text = LM.message("login_button")
                self.login_button.disabled = False
        
        self.auth_controller.login(email, password, auth_callback)
    
    def _show_error(self):
        """Display error message with animation."""
        if self.show_error > 0:
            Animation(show_error=0, duration=0.2).start(self)
            Clock.schedule_once(lambda dt: self._fade_in_error(), 0.3)
        else:
            self._fade_in_error()
    
    def _fade_in_error(self):
        """Animate error message fade-in."""
        Animation(show_error=1, duration=0.3).start(self)
        Clock.schedule_once(
            lambda dt: Animation(show_error=0, duration=0.5).start(self), 
            5
        )