from app.views.screens import BaseScreen
from kivy.properties import StringProperty, NumericProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder

# Load kv file
Builder.load_file('kv/login_screen.kv')

class LoginScreen(BaseScreen):
    error_message = StringProperty("")
    show_error = NumericProperty(0)
    
    def go_back(self):
        self.switch_screen('first_screen', 'right')
    
    def go_to_registration(self):
        self.switch_screen('reg_screen', 'left')
    
    def login(self):
        email = self.email_input.text
        password = self.password_input.text
        
        if not email:
            self.error_message = "Будь ласка, введіть email"
            self._show_error()
            return
        
        if not password:
            self.error_message = "Будь ласка, введіть пароль"
            self._show_error()
            return
        
        self.login_button.text = "Авторизація..."
        self.login_button.disabled = True
    
        def authenticate(dt):
            success = True
            if success:
                self.switch_screen('main_screen', 'left')
            else:
                self.error_message = "Невірний email або пароль"
                self._show_error()
                self.login_button.text = "Увійти"
                self.login_button.disabled = False

        Clock.schedule_once(authenticate, 1)
    
    def _show_error(self):
        if self.show_error > 0:
            Animation(show_error=0, duration=0.2).start(self)
            Clock.schedule_once(lambda dt: self._fade_in_error(), 0.3)
        else:
            self._fade_in_error()
    
    def _fade_in_error(self):
        Animation(show_error=1, duration=0.3).start(self)
        Clock.schedule_once(
            lambda dt: Animation(show_error=0, duration=0.5).start(self), 
            5
        )