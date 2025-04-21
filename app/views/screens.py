from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import StringProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget
from kivy.graphics import Color, Ellipse
from kivy.metrics import dp
import random

class BaseScreen(Screen):
    opacity = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(BaseScreen, self).__init__(**kwargs)
        Animation(opacity=1, d=0.8).start(self)
        Clock.schedule_once(self._animate_particles, 0.5)
    
    def _animate_particles(self, dt):
        import random
        
        for _ in range(20):
            particle = Widget(
                size_hint=(None, None),
                size=(dp(3), dp(3)),
                pos_hint={'x': random.random(), 'y': random.random()}
            )
            
            with particle.canvas:
                color_choice = random.choice([
                    get_color_from_hex('#FF7043'),
                    get_color_from_hex('#FFB74D'),
                    get_color_from_hex('#0F7055'),
                    get_color_from_hex('#FFFFFF')
                ])
                
                r, g, b = color_choice[0:3]
                alpha = random.uniform(0.1, 0.4)
                
                Color(r, g, b, alpha)
                Ellipse(pos=particle.pos, size=particle.size)
            
            self.add_widget(particle)
            
            anim_duration = random.uniform(5, 15)
            anim_x = random.uniform(0, 1)
            anim_y = random.uniform(0, 1)
            
            anim = Animation(
                pos_hint={'x': anim_x, 'y': anim_y},
                duration=anim_duration
            )
            anim.repeat = True
            anim.start(particle)
    
    def switch_screen(self, screen_name, direction='left'):
        if self.manager:
            self.manager.transition = SlideTransition(direction=direction)
            self.manager.current = screen_name