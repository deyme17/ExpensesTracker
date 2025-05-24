from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle

from app.views.widgets.buttons.styled_button import RoundedButton
from app.utils.theme import get_primary_color, get_text_primary_color
from utils.language_mapper import LanguageMapper as LM

class ConfirmDeletePopup(ModalView):
    def __init__(self, on_confirm, on_cancel=None, message=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.85, None)
        self.height = dp(220)
        self.auto_dismiss = False
        self.background = ''
        self.background_color = (0, 0, 0, 0)
        self.overlay_color = (0, 0, 0, 0.65)

        layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(20))

        with layout.canvas.before:
            Color(rgba=get_primary_color())
            self.rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(16)])

        layout.bind(pos=self._update_rect, size=self._update_rect)

        label_text = message if message else LM.message("confirmation_delete")

        label = Label(
            text=label_text,
            halign="center",
            valign="middle",
            color=get_text_primary_color(),
            font_size=sp(16),
            size_hint_y=None,
            height=dp(80),
            text_size=(dp(250), None)
        )

        buttons = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(12))

        cancel_btn = RoundedButton(
            text=f"[b]{LM.message('no_button')}[/b]",
            bg_color="#777777",
            markup=True,
            on_press=lambda x: (self.dismiss(), on_cancel() if on_cancel else None)
        )

        confirm_btn = RoundedButton(
            text=f"[b]{LM.message('yes_button')}[/b]",
            bg_color="#F44336",
            markup=True,
            on_press=lambda x: (self.dismiss(), on_confirm())
        )

        buttons.add_widget(cancel_btn)
        buttons.add_widget(confirm_btn)

        layout.add_widget(Widget())
        layout.add_widget(label)
        layout.add_widget(buttons)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size
