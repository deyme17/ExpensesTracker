from kivy.properties import StringProperty, NumericProperty, ObjectProperty
from kivy.uix.button import Button
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.lang import Builder

from app.views.screens.base_screen import BaseScreen
from app.utils.validators import validate_registration_inputs
from app.views.widgets.popups.info_popup import MonobankTokenInfoPopup
from app.utils.language_mapper import LanguageMapper as LM

Builder.load_file("kv/register_screen.kv")


class RegistrationScreen(BaseScreen):
    error_message = StringProperty("")
    show_error = NumericProperty(0)

    def __init__(self, auth_controller, **kwargs):
        super(RegistrationScreen, self).__init__(**kwargs)
        self.auth_controller=auth_controller
        self._add_back_button()

    def _add_back_button(self):
        btn = Button(
            text="<", font_size="24sp", color=get_color_from_hex("#FFFFFF"),
            size_hint=(None, None), size=(dp(50), dp(50)),
            pos_hint={"x": 0.02, "top": 0.98}, background_color=(0, 0, 0, 0),
            on_release=self.go_back
        )
        with btn.canvas.before:
            from kivy.graphics import Color, Ellipse
            Color(rgba=(1, 1, 1, 0.15))
            self.back_ellipse = Ellipse(pos=btn.pos, size=btn.size)
        btn.bind(pos=self.update_back_button, size=self.update_back_button)
        Clock.schedule_once(lambda dt: self.add_widget(btn), 0.1)

    def update_back_button(self, instance, value):
        if hasattr(self, "back_ellipse"):
            self.back_ellipse.pos = instance.pos
            self.back_ellipse.size = instance.size

    def on_enter(self):
        super().on_enter()
        for field in ("email_input", "password_input", "confirm_password_input", "monobank_token_input"):
            if hasattr(self, field):
                getattr(self, field).text = ""
        if hasattr(self, "register_button"):
            self.register_button.text = LM.message("register_button_action")
            self.register_button.disabled = False
        self.error_message = ""
        self.show_error = 0

    def go_back(self, *args):
        self.switch_screen("first_screen", "right")

    def go_to_login(self, *args):
        self.switch_screen("login_screen", "right")

    def show_token_info(self, *args):
        MonobankTokenInfoPopup().open()

    def _update_modal_rect(self, instance, value):
        if hasattr(self, "rect"):
            self.rect.pos = instance.pos
            self.rect.size = instance.size

    def register(self, *args):
        inputs = {
            "email": self.email_input.text.strip(),
            "password": self.password_input.text,
            "confirm_password": self.confirm_password_input.text,
            "monobank_token": self.monobank_token_input.text.strip()
        }
        valid, message = validate_registration_inputs(inputs)
        if not valid:
            self.error_message = message
            self._show_error()
            return

        self.register_button.text = LM.message("register_button") + "..."
        self.register_button.disabled = True

        def reg_callback(success, message):
            if success:
                self.switch_screen("splash_screen", "left")
            else:
                self.error_message = message
                self._show_error()
                self.register_button.text = LM.message("register_button_action")
                self.register_button.disabled = False

        if self.auth_controller:
            self.auth_controller.register(
                email=inputs["email"], password=inputs["password"],
                confirm_password=inputs["confirm_password"],
                monobank_token=inputs["monobank_token"], callback=reg_callback
            )
        else:
            self.error_message = LM.message("registration_error_generic")
            self._show_error()
            self.register_button.text = LM.message("register_button_action")
            self.register_button.disabled = False

    def _show_error(self):
        if self.show_error > 0:
            Animation(show_error=0, duration=0.2).start(self)
            Clock.schedule_once(lambda dt: self._fade_in_error(), 0.3)
        else:
            self._fade_in_error()

    def _fade_in_error(self):
        Animation(show_error=1, duration=0.3).start(self)
        Clock.schedule_once(lambda dt: Animation(show_error=0, duration=0.5).start(self), 5)