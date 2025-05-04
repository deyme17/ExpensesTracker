from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ListProperty, NumericProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

from app.utils.theme import (
    PRIMARY_COLOR, SECONDARY_COLOR, FONT_SIZE_MEDIUM
)


class SegmentedButton(BoxLayout):
    """
    A segmented button for selecting between multiple options.
    """
    options = ListProperty([])
    selected_index = NumericProperty(0)
    bg_color = StringProperty(SECONDARY_COLOR)
    selected_color = StringProperty(PRIMARY_COLOR)
    text_color = StringProperty('#0A4035')
    selected_text_color = StringProperty('#FFFFFF')
    
    def __init__(self, **kwargs):
        kwargs.setdefault('orientation', 'horizontal')
        kwargs.setdefault('size_hint_y', None)
        kwargs.setdefault('height', dp(45))
        kwargs.setdefault('padding', dp(2))
        kwargs.setdefault('spacing', dp(2))
        
        super(SegmentedButton, self).__init__(**kwargs)
        
        # bind properties
        self.bind(options=self._update_buttons)
        self.bind(selected_index=self._update_selection)
        
        Clock.schedule_once(lambda dt: self._update_buttons(), 0)
    
    def _update_buttons(self, *args):
        """Update buttons when options change."""
        self.clear_widgets()
        
        for i, option in enumerate(self.options):
            button = Button(
                text=option,
                background_color=(0, 0, 0, 0), 
                color=get_color_from_hex(self.selected_text_color if i == self.selected_index else self.text_color),
                font_size=sp(FONT_SIZE_MEDIUM),
                size_hint_x=1/len(self.options) if self.options else 1
            )
            
            def create_callback(idx):
                return lambda instance: self.select(idx)
            
            button.bind(on_press=create_callback(i))
            
            with button.canvas.before:
                Color(*get_color_from_hex(self.selected_color if i == self.selected_index else self.bg_color))
                
                # rounded corners
                if i == 0:                          # first button
                    radius = [dp(8), 0, 0, dp(8)]
                elif i == len(self.options) - 1:    # last button
                    radius = [0, dp(8), dp(8), 0]
                else:                               # mid button
                    radius = [0, 0, 0, 0]
                
                RoundedRectangle(
                    pos=button.pos,
                    size=button.size,
                    radius=radius
                )
            
            button.bind(pos=self._update_button_bg, size=self._update_button_bg)
            
            self.add_widget(button)
    
    def _update_button_bg(self, instance, value):
        """Update button background when position or size changes."""
        instance.canvas.before.clear()
        
        try:
            idx = self.children.index(instance)
            idx = len(self.children) - 1 - idx
        except ValueError:
            return
        
        with instance.canvas.before:
            Color(*get_color_from_hex(self.selected_color if idx == self.selected_index else self.bg_color))
            
            # rounded corners
            if idx == 0:                        # first button
                radius = [dp(8), 0, 0, dp(8)]
            elif idx == len(self.options) - 1:  # last button
                radius = [0, dp(8), dp(8), 0]
            else:                               # mid button
                radius = [0, 0, 0, 0]
            
            RoundedRectangle(
                pos=instance.pos,
                size=instance.size,
                radius=radius
            )
    
    def _update_selection(self, instance, value):
        """Update button selection when selected_index changes."""
        self._update_buttons()
    
    def select(self, index):
        """Select a specific option by index."""
        if 0 <= index < len(self.options):
            self.selected_index = index