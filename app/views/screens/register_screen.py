from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.modalview import ModalView
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.graphics import Color, Ellipse, RoundedRectangle
from kivy.lang import Builder

from app.views.screens.base_screen import BaseScreen
from app.views.widgets.custom_inputs import StyledTextInput
from app.views.widgets.custom_buttons import RoundedButton
from app.utils.theme import get_text_primary_color, get_accent_color

# Load kv file
Builder.load_file('kv/register_screen.kv')


class RegistrationScreen(BaseScreen):
    """
    Screen for user registration.
    
    Handles the UI representation of the registration process, delegating actual
    account creation logic to the AuthController.
    """
    error_message = StringProperty("")
    show_error = NumericProperty(0)
    controller = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(RegistrationScreen, self).__init__(**kwargs)
        
        # back button
        self.back_button = Button(
            text='<',
            font_size='24sp',
            color=get_color_from_hex('#FFFFFF'),
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={'x': 0.02, 'top': 0.98},
            background_color=(0, 0, 0, 0),
            on_release=self.go_back
        )
        
        with self.back_button.canvas.before:
            Color(rgba=(1, 1, 1, 0.15))
            self.back_ellipse = Ellipse(pos=self.back_button.pos, size=self.back_button.size)
        
        self.back_button.bind(pos=self.update_back_button, size=self.update_back_button)

        Clock.schedule_once(lambda dt: self.add_widget(self.back_button), 0.1)
    
    def update_back_button(self, instance, value):
        """Update back button's ellipse when position or size changes."""
        if hasattr(self, 'back_ellipse'):
            self.back_ellipse.pos = instance.pos
            self.back_ellipse.size = instance.size
    
    def on_enter(self):
        """Reset fields when screen is entered."""
        super(RegistrationScreen, self).on_enter()
        
        # reset input fields and buttons
        if hasattr(self, 'name_input'):
            self.name_input.text = ""
        if hasattr(self, 'email_input'):
            self.email_input.text = ""
        if hasattr(self, 'password_input'):
            self.password_input.text = ""
        if hasattr(self, 'confirm_password_input'):
            self.confirm_password_input.text = ""
        if hasattr(self, 'monobank_token_input'):
            self.monobank_token_input.text = ""
        if hasattr(self, 'register_button'):
            self.register_button.text = "Зареєструватись"
            self.register_button.disabled = False
        
        # error message
        self.error_message = ""
        self.show_error = 0
    
    def go_back(self, *args):
        """Navigate back to the first screen."""
        self.switch_screen('first_screen', 'right')
    
    def go_to_login(self, *args):
        """Navigate to the login screen."""
        self.switch_screen('login_screen', 'right')
    
    def show_token_info(self, *args):
        """Show information about Monobank API token."""
        modal = ModalView(size_hint=(0.8, 0.5))
        
        content = BoxLayout(
            orientation='vertical',
            padding=dp(20),
            spacing=dp(10)
        )
        
        with content.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            RoundedRectangle(pos=content.pos, size=content.size, radius=[dp(10)])
        
        # title
        title = Label(
            text='Монобанк API Токен',
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(40),
            color=get_color_from_hex('#FFFFFF')
        )
        
        # info text
        info = Label(
            text='Монобанк API токен дозволяє автоматично імпортувати ваші транзакції. '
                 'Ви можете отримати його в додатку Монобанк або на веб-сайті api.monobank.ua.\n\n'
                 'Токен не є обов\'язковим для реєстрації, але надає додаткові можливості.',
            font_size='16sp',
            halign='left',
            valign='top',
            size_hint_y=None,
            height=dp(150),
            text_size=(modal.width * 0.7, None),
            color=get_color_from_hex('#FFFFFF')
        )
        
        # close button
        close_button = RoundedButton(
            text='Зрозуміло',
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            pos_hint={'center_x': 0.5},
            bg_color='#FF7043'
        )
        close_button.bind(on_press=lambda x: modal.dismiss())
        
        # add widgets to content
        content.add_widget(title)
        content.add_widget(info)
        content.add_widget(close_button)
        
        modal.add_widget(content)
        
        modal.open()
    
    def register(self, *args):     # TODO
        """
        Process registration attempt.
        
        Validates input fields and delegates account creation to the controller.
        """
        name = self.name_input.text.strip()
        email = self.email_input.text.strip()
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text
        monobank_token = self.monobank_token_input.text.strip()
      
        if not name:
            self.error_message = "Будь ласка, введіть ім'я"
            self._show_error()
            return
        
        if not email:
            self.error_message = "Будь ласка, введіть email"
            self._show_error()
            return
        
        if '@' not in email or '.' not in email:
            self.error_message = "Будь ласка, введіть коректний email"
            self._show_error()
            return
        
        if not password:
            self.error_message = "Будь ласка, введіть пароль"
            self._show_error()
            return
        
        if len(password) < 6:
            self.error_message = "Пароль має бути не менше 6 символів"
            self._show_error()
            return
        
        if password != confirm_password:
            self.error_message = "Паролі не співпадають"
            self._show_error()
            return
        
        self.register_button.text = "Реєстрація..."
        self.register_button.disabled = True
        
        def reg_callback(success, message):
            if success:
                self.switch_screen('transactions_screen', 'left')
            else:
                self.error_message = message
                self._show_error()
                self.register_button.text = "Зареєструватись"
                self.register_button.disabled = False
        
        if self.controller:
            self.controller.register(
                name=name,
                email=email,
                password=password,
                confirm_password=confirm_password,
                monobank_token=monobank_token if monobank_token else None,
                callback=reg_callback
            )
        else:
            self.error_message = "Внутрішня помилка системи"
            self._show_error()
            self.register_button.text = "Зареєструватись"
            self.register_button.disabled = False
    
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