from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.modalview import ModalView
from kivy.uix.button import Button
from kivy.properties import StringProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from app.views.widgets.buttons.rounded_button import StyledButton


from app.utils.theme import (
    get_background_color, get_text_primary_color,
    FONT_SIZE_MEDIUM
)

class ConfirmationPopup(Popup):
    """Popup for confirming an action."""
    message = StringProperty("")
    
    def __init__(self, message, on_confirm, on_cancel=None, **kwargs):
        super(ConfirmationPopup, self).__init__(**kwargs)
        self.message = message
        self.title = "Підтвердження"
        self.size_hint = (0.8, 0.4)
        self.background = ""
        self.background_color = (0, 0, 0, 0)
        self.auto_dismiss = False
        
        self.on_confirm_callback = on_confirm
        self.on_cancel_callback = on_cancel
        
        content = self._create_content()
        self.content = content
    
    def _create_content(self):
        """Create the content of the confirmation popup."""
        content = BoxLayout(orientation='vertical', spacing=dp(15), padding=[dp(20), dp(20), dp(20), dp(20)])
        
        # message label
        label = Label(
            text=self.message,
            font_size=sp(FONT_SIZE_MEDIUM),
            color=get_text_primary_color(),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(60)
        )
        label.bind(
            size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None))
        )
        
        # buttons
        buttons_box = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(15))
        
        cancel_button = StyledButton(
            text='Скасувати',
            bg_color='#445555',
            size_hint_y=None,
            height=dp(45),
            font_size=sp(FONT_SIZE_MEDIUM)
        )
        
        confirm_button = StyledButton(
            text='Підтвердити',
            bg_color='#0F7055',
            size_hint_y=None,
            height=dp(45),
            font_size=sp(FONT_SIZE_MEDIUM)
        )
        
        cancel_button.bind(on_press=self._on_cancel)
        confirm_button.bind(on_press=self._on_confirm)
        
        buttons_box.add_widget(cancel_button)
        buttons_box.add_widget(confirm_button)
        
        content.add_widget(label)
        content.add_widget(buttons_box)
        
        return content
    
    def _on_confirm(self, instance):
        """Called when the confirm button is pressed."""
        self.dismiss()
        if self.on_confirm_callback:
            self.on_confirm_callback()
    
    def _on_cancel(self, instance):
        """Called when the cancel button is pressed."""
        self.dismiss()
        if self.on_cancel_callback:
            self.on_cancel_callback()
    
    def on_open(self):
        """Called when the popup is opened."""
        super(ConfirmationPopup, self).on_open()
        
        with self.canvas.before:
            self._bg_color = Color(rgba=get_background_color())
            self._bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])

        self.bind(pos=self._update_canvas, size=self._update_canvas)
    
    def _update_canvas(self, instance, value):
        """Update the canvas when size or position changes."""
        if hasattr(self, '_bg_rect'):
            self._bg_rect.pos = instance.pos
            self._bg_rect.size = instance.size
