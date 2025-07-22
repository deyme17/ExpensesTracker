from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.properties import StringProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.uix.anchorlayout import AnchorLayout
from kivy.metrics import dp

from app.views.widgets.buttons.styled_button import RoundedButton
from app.views.widgets.buttons.styled_button import StyledButton
from app.utils.theme import get_background_color
from app.utils.language_mapper import LanguageMapper as LM


class InfoPopup(Popup):
    """Popup for displaying informational content."""
    title_text = StringProperty("")
    
    def __init__(self, title_text, content_widget, **kwargs):
        super(InfoPopup, self).__init__(**kwargs)
        self.title_text = title_text
        self.title = title_text
        self.size_hint = (0.9, 0.8)
        self.background = ""
        self.background_color = (0, 0, 0, 0)
        
        container = BoxLayout(orientation="vertical", spacing=dp(10), padding=dp(15))
        container.add_widget(content_widget)
        
        close_button = StyledButton(
            text=LM.message("close_button"),
            bg_color="#445555",
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            pos_hint={"center_x": 0.5}
        )
        close_button.bind(on_press=self.dismiss)
        
        container.add_widget(close_button)
        self.content = container
    
    def on_open(self):
        """Called when the popup is opened."""
        super(InfoPopup, self).on_open()
        
        with self.canvas.before:
            self._bg_color = Color(rgba=get_background_color())
            self._bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
        
        self.bind(pos=self._update_canvas, size=self._update_canvas)
    
    def _update_canvas(self, instance, value):
        """Update the canvas when size or position changes."""
        if hasattr(self, "_bg_rect"):
            self._bg_rect.pos = instance.pos
            self._bg_rect.size = instance.size

class MonobankTokenInfoPopup(ModalView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.8, 0.5)

        layout = BoxLayout(orientation="vertical", padding=dp(20), spacing=dp(10))

        with layout.canvas.before:
            from kivy.graphics import Color, RoundedRectangle
            Color(rgba=get_color_from_hex('#0A4035'))
            self.rect = RoundedRectangle(pos=layout.pos, size=layout.size, radius=[dp(10)])
        layout.bind(size=self._update_rect, pos=self._update_rect)

        layout.add_widget(Label(
            text=LM.message("mono_token_label"),
            font_size="20sp",
            bold=True,
            size_hint_y=None,
            height=dp(40),
            color=get_color_from_hex('#FFFFFF')
        ))

        token_label = Label(
            text=LM.message("mono_token_hint"),
            font_size='16sp',
            halign='left',
            valign='top',
            color=get_color_from_hex('#FFFFFF')
        )
        token_label.bind(size=lambda inst, val: setattr(inst, "text_size", (inst.width, None)))
        layout.add_widget(token_label)

        button = RoundedButton(
            text=LM.message("understand_label"),
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            bg_color='#FF7043'
        )
        button.bind(on_press=lambda x: self.dismiss())

        button_container = AnchorLayout(size_hint_y=None, height=dp(60))
        button_container.add_widget(button)
        layout.add_widget(button_container)

        self.add_widget(layout)

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size