from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.properties import StringProperty, NumericProperty
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp

from app.utils.theme import (
    get_error_color, get_success_color, 
    get_background_color, get_text_primary_color,
    get_secondary_color, get_text_dark_color,
    FONT_SIZE_MEDIUM
)


class BasePopup(Popup):
    """Base class for custom popups."""
    message = StringProperty("")
    
    def __init__(self, message, **kwargs):
        super(BasePopup, self).__init__(**kwargs)
        self.message = message
        self.title = ""
        self.size_hint = (0.8, 0.3)
        self.background = ""
        self.background_color = (0, 0, 0, 0)
        self.auto_dismiss = True
        
        # content setup
        content = self._create_content()
        self.content = content
        
        # auto-dismiss after 2 seconds
        Clock.schedule_once(lambda dt: self.dismiss(), 2)
    
    def _create_content(self):
        """Create the content of the popup. Override in subclasses."""
        content = BoxLayout(orientation='vertical', padding=dp(10))
        
        label = Label(
            text=self.message,
            color=get_text_primary_color(),
            font_size=sp(FONT_SIZE_MEDIUM),
            halign='center',
            valign='middle'
        )
        label.bind(size=label.setter('text_size'))
        
        content.add_widget(label)
        return content
    
    def on_open(self):
        """Called when the popup is opened."""
        super(BasePopup, self).on_open()
        
        with self.canvas.before:
            self._bg_color = Color(rgba=self._get_background_color())
            self._bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])

        self.bind(pos=self._update_canvas, size=self._update_canvas)
    
    def _update_canvas(self, instance, value):
        """Update the canvas when size or position changes."""
        if hasattr(self, '_bg_rect'):
            self._bg_rect.pos = instance.pos
            self._bg_rect.size = instance.size
    
    def _get_background_color(self):
        """Get the background color for the popup. Override in subclasses."""
        return get_background_color()


class ErrorPopup(BasePopup):
    """Popup for displaying error messages."""
    
    def __init__(self, message, **kwargs):
        super(ErrorPopup, self).__init__(message, **kwargs)
        self.title = "Помилка"
    
    def _get_background_color(self):
        """Get the background color for error popups."""
        return get_error_color()


class SuccessPopup(BasePopup):
    """Popup for displaying success messages."""
    
    def __init__(self, message, **kwargs):
        super(SuccessPopup, self).__init__(message, **kwargs)
        self.title = "Успіх"
    
    def _get_background_color(self):
        """Get the background color for success popups."""
        return get_success_color()


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


class StyledButton(Button):
    """Custom styled button with rounded corners and background color."""
    
    def __init__(self, bg_color, **kwargs):
        super(StyledButton, self).__init__(**kwargs)
        self.background_color = (0, 0, 0, 0)
        self.bg_color = bg_color
        self.color = get_text_primary_color()
        self.bold = True
        
        self.bind(size=self.update_background, pos=self.update_background)
        
        Clock.schedule_once(lambda dt: self.update_background(), 0)
    
    def update_background(self, *args):
        """Update the button's background canvas."""
        self.canvas.before.clear()
        with self.canvas.before:
            Color(rgba=get_color_from_hex(self.bg_color))
            RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])


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
        
        container = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(15))
        container.add_widget(content_widget)
        
        close_button = StyledButton(
            text="Закрити",
            bg_color='#445555',
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            pos_hint={'center_x': 0.5}
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
        if hasattr(self, '_bg_rect'):
            self._bg_rect.pos = instance.pos
            self._bg_rect.size = instance.size