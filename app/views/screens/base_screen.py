from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.graphics import Color, Ellipse
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget
from kivy.metrics import dp

import random as rnd


class BaseScreen(Screen):
    opacity = NumericProperty(0)
    logout_callback = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        self._animate_entrance()
        Clock.schedule_once(self._animate_particles, 0.5)
    
    def on_enter(self):
        """Called when the screen enters the view."""
        pass
    
    def on_leave(self):
        """Called when the screen leaves the view."""
        pass
    
    def _animate_entrance(self):
        """Animate the screen's entrance with a fade-in effect."""
        Animation(opacity=1, d=0.8).start(self)
    
    def _animate_particles(self, dt):
        """Create animated background particles for visual effect."""
        for _ in range(20):
            particle = Widget(
                size_hint=(None, None),
                size=(dp(3), dp(3)),
                pos_hint={'x': rnd.random(), 'y': rnd.random()}
            )
            
            with particle.canvas:
                color_choice = rnd.choice([
                    get_color_from_hex('#FF7043'),
                    get_color_from_hex('#FFB74D'),
                    get_color_from_hex('#0F7055'),
                    get_color_from_hex('#FFFFFF')
                ])
                
                r, g, b = color_choice[0:3]
                alpha = rnd.uniform(0.1, 0.4)
                
                Color(r, g, b, alpha)
                Ellipse(pos=particle.pos, size=particle.size)
            
            self.add_widget(particle)
            
            anim_duration = rnd.uniform(5, 15)
            anim_x = rnd.uniform(0, 1)
            anim_y = rnd.uniform(0, 1)
            
            anim = Animation(
                pos_hint={'x': anim_x, 'y': anim_y},
                duration=anim_duration
            )
            anim.repeat = True
            anim.start(particle)
    
    def switch_screen(self, screen_name, direction='left'):
        """
        Switch to another screen with a slide transition.
        
        Args:
            screen_name (str): The name of the screen to switch to
            direction (str): The direction of the slide transition (left, right, up, down)
        """
        if self.manager:
            self.manager.transition = SlideTransition(direction=direction)
            self.manager.current = screen_name
    
    def show_error_message(self, message):
        """Display an error message with slight delay to allow UI to update."""
        from app.views.widgets.popups.alert_popup import ErrorPopup
        Clock.schedule_once(lambda dt: ErrorPopup(message=message).open(), 0.2)

    def show_success_message(self, message):
        """Display a success message with slight delay to allow UI to update."""
        from app.views.widgets.popups.alert_popup import SuccessPopup
        Clock.schedule_once(lambda dt: SuccessPopup(message=message).open(), 0.2)

    def show_menu(self, *args):
        from app.views.widgets.popups.menu_popup import MenuPopup
        popup = MenuPopup(on_logout=self._logout, on_exit=self._exit_app)
        popup.open()

    def _logout(self):
        if self.logout_callback:
            self.logout_callback()
        self.switch_screen("first_screen", "right")

    def _exit_app(self):
        from kivy.core.window import Window
        Window.close()