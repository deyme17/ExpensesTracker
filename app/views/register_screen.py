from app.views.screens import BaseScreen
from kivy.properties import StringProperty, NumericProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.uix.button import Button
from kivy.graphics import Color, Ellipse, RoundedRectangle
from kivy.metrics import dp
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label

# Load kv file
Builder.load_file('kv/register_screen.kv')

class RegistrationScreen(BaseScreen):
    error_message = StringProperty("")
    show_error = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(RegistrationScreen, self).__init__(**kwargs)
        
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
        if hasattr(self, 'back_ellipse'):
            self.back_ellipse.pos = instance.pos
            self.back_ellipse.size = instance.size
    
    def go_back(self, *args):
        self.switch_screen('first_screen', 'right')
    
    def go_to_login(self, *args):
        self.switch_screen('login_screen', 'right')
    
    def show_token_info(self, *args):
        modal = ModalView(size_hint=(0.8, 0.5))
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        with content.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            RoundedRectangle(pos=content.pos, size=content.size, radius=[dp(10)])
        
        title = Label(
            text='Монобанк API Токен',
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(40),
            color=get_color_from_hex('#FFFFFF')
        )
        
        info = Label(
            text='Монобанк API токен дозволяє автоматично імпортувати ваші транзакції. '
                 'Ви можете отримати його в додатку Монобанк або на веб-сайті api.monobank.ua.\n\n',
            font_size='16sp',
            halign='left',
            valign='top',
            size_hint_y=None,
            height=dp(150),
            text_size=(modal.width * 0.7, None),
            color=get_color_from_hex('#FFFFFF')
        )
        
        close_button = Button(
            text='Зрозуміло',
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            pos_hint={'center_x': 0.5},
            background_color=get_color_from_hex('#FF7043')
        )
        close_button.bind(on_press=lambda x: modal.dismiss())
        
        content.add_widget(title)
        content.add_widget(info)
        content.add_widget(close_button)
        modal.add_widget(content)
        modal.open()
    
    def register(self, *args):
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
        
        def process_registration(dt):
            success = True
            
            if success:
                self.switch_screen('main_screen', 'left')
            else:
                self.error_message = "Помилка при реєстрації. Спробуйте пізніше."
                self._show_error()
                self.register_button.text = "Зареєструватись"
                self.register_button.disabled = False
        
        Clock.schedule_once(process_registration, 1.5)
    
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