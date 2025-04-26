from kivy.uix.button import Button
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty
from kivy.graphics import Color, RoundedRectangle, Line, Ellipse
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.clock import Clock

from app.utils.theme import (
    get_primary_color, get_secondary_color, get_accent_color, 
    get_text_primary_color, get_text_dark_color,
    PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR,
    FONT_SIZE_MEDIUM
)


class RoundedButton(Button):
    """
    A button with rounded corners and customizable colors.
    """
    bg_color = StringProperty(PRIMARY_COLOR)
    bg_color_down = StringProperty('')
    border_radius = ListProperty([dp(10)])
    text_color = ListProperty([1, 1, 1, 1])
    
    def __init__(self, **kwargs):
        kwargs.setdefault('background_color', (0, 0, 0, 0))
        kwargs.setdefault('color', kwargs.get('text_color', [1, 1, 1, 1]))
        kwargs.setdefault('halign', 'center')
        kwargs.setdefault('valign', 'middle')
        kwargs.setdefault('font_size', sp(FONT_SIZE_MEDIUM))
        
        super(RoundedButton, self).__init__(**kwargs)
        
        if not self.bg_color_down:
            color = get_color_from_hex(self.bg_color)
            if not self.bg_color_down:
                if self.bg_color.startswith('#'):
                    self.bg_color_down = '#0A352D'
                else:
                    self.bg_color_down = self.bg_color
            
        # bind properties
        self.bind(pos=self._update_canvas)
        self.bind(size=self._update_canvas)
        self.bind(state=self._update_canvas)
        
        Clock.schedule_once(lambda dt: self._update_canvas(), 0)
    
    def _update_canvas(self, *args):
        """Update the button's background canvas."""
        self.canvas.before.clear()
        with self.canvas.before:
            if self.state == 'down':
                Color(*get_color_from_hex(self.bg_color_down))
            else:
                Color(*get_color_from_hex(self.bg_color))
            
            RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=self.border_radius
            )


class IconButton(BoxLayout):
    """
    A button with an icon and optional text.
    """
    text = StringProperty('')
    icon = StringProperty('')
    bg_color = StringProperty(PRIMARY_COLOR)
    is_selected = BooleanProperty(False)
    
    def __init__(self, **kwargs):
        kwargs.setdefault('orientation', 'vertical')
        kwargs.setdefault('size_hint', (None, None))
        kwargs.setdefault('size', (dp(60), dp(60)))
        kwargs.setdefault('spacing', dp(5))
        
        super(IconButton, self).__init__(**kwargs)
        
        # bind properties
        self.bind(pos=self._update_canvas)
        self.bind(size=self._update_canvas)
        self.bind(is_selected=self._update_canvas)
        self.bind(text=self._update_text)
        self.bind(icon=self._update_icon)
        
        # icon widget
        self.icon_widget = Label(
            text=self.icon,
            font_size=sp(24),
            color=get_text_primary_color(),
            size_hint=(1, 0.7)
        )
        
        # text label
        self.text_label = Label(
            text=self.text,
            font_size=sp(12),
            color=get_text_primary_color(),
            size_hint=(1, 0.3)
        )
        
        self.add_widget(self.icon_widget)
        self.add_widget(self.text_label)
        
        Clock.schedule_once(lambda dt: self._update_canvas(), 0)
    
    def _update_canvas(self, *args):
        """Update the button's background canvas."""
        self.canvas.before.clear()
        with self.canvas.before:
            if self.is_selected:
                Color(*get_color_from_hex(ACCENT_COLOR))
                RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=[dp(10)]
                )
            else:
                Color(*get_color_from_hex(self.bg_color))
                RoundedRectangle(
                    pos=self.pos,
                    size=self.size,
                    radius=[dp(10)]
                )
    
    def _update_text(self, instance, value):
        """Update text label when text property changes."""
        self.text_label.text = value
    
    def _update_icon(self, instance, value):
        """Update icon when icon property changes."""
        self.icon_widget.text = value
    
    def on_touch_down(self, touch):
        """Handle touch events."""
        if self.collide_point(*touch.pos):
            self.is_selected = True
            return True
        return super(IconButton, self).on_touch_down(touch)


class FloatingActionButton(Button):
    """
    A circular floating action button.
    """
    bg_color = StringProperty(ACCENT_COLOR)
    icon = StringProperty('+')
    
    def __init__(self, **kwargs):
        kwargs.setdefault('background_color', (0, 0, 0, 0))
        kwargs.setdefault('size_hint', (None, None))
        kwargs.setdefault('size', (dp(56), dp(56)))
        kwargs.setdefault('text', self.icon)
        kwargs.setdefault('font_size', sp(30))
        kwargs.setdefault('bold', True)
        kwargs.setdefault('color', get_text_primary_color())
        
        super(FloatingActionButton, self).__init__(**kwargs)
        
        # bind properties
        self.bind(pos=self._update_canvas)
        self.bind(size=self._update_canvas)
        self.bind(state=self._update_canvas)
        
        Clock.schedule_once(lambda dt: self._update_canvas(), 0)
    
    def _update_canvas(self, *args):
        """Update the button's background canvas."""
        self.canvas.before.clear()
        with self.canvas.before:
            Color(0, 0, 0, 0.2)
            Ellipse(pos=(self.x + dp(2), self.y - dp(2)), size=self.size)
            
            if self.state == 'down':
                r, g, b = get_color_from_hex(self.bg_color)[:3]
                Color(r*0.8, g*0.8, b*0.8, 1)
            else:
                Color(*get_color_from_hex(self.bg_color))
            
            Ellipse(pos=self.pos, size=self.size)


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


class TabButton(BoxLayout):
    """
    A button for a tab interface.
    """
    text = StringProperty('')
    icon = StringProperty('')
    is_selected = BooleanProperty(False)
    badge_count = StringProperty('')
    
    def __init__(self, **kwargs):
        kwargs.setdefault('orientation', 'vertical')
        kwargs.setdefault('size_hint_x', None)
        kwargs.setdefault('width', dp(80))
        kwargs.setdefault('padding', dp(5))
        
        super(TabButton, self).__init__(**kwargs)
        
        # icon label
        self.icon_label = Label(
            text=self.icon,
            font_size=sp(24),
            color=get_text_primary_color(),
            size_hint_y=0.6
        )
        
        # text label
        self.text_label = Label(
            text=self.text,
            font_size=sp(12),
            color=get_text_primary_color(),
            size_hint_y=0.4
        )
        
        self.add_widget(self.icon_label)
        self.add_widget(self.text_label)
        
        # bind properties
        self.bind(text=self._update_text)
        self.bind(icon=self._update_icon)
        self.bind(is_selected=self._update_canvas)
        self.bind(pos=self._update_canvas, size=self._update_canvas)
        self.bind(badge_count=self._update_badge)
        
        Clock.schedule_once(lambda dt: self._update_canvas(), 0)
    
    def _update_canvas(self, *args):
        """Update the button's canvas."""
        self.canvas.before.clear()
        with self.canvas.before:
            if self.is_selected:
                Color(*get_color_from_hex(ACCENT_COLOR))
                Line(
                    points=[
                        self.x + dp(10), self.y,
                        self.x + self.width - dp(10), self.y
                    ],
                    width=dp(2)
                )
    
    def _update_text(self, instance, value):
        """Update text label when text property changes."""
        self.text_label.text = value
    
    def _update_icon(self, instance, value):
        """Update icon label when icon property changes."""
        self.icon_label.text = value
    
    def _update_badge(self, instance, value):
        """Update badge when badge_count property changes."""
        pass
    
    def on_touch_down(self, touch):
        """Handle touch events."""
        if self.collide_point(*touch.pos):
            self.is_selected = True
            return True
        return super(TabButton, self).on_touch_down(touch)