from app.views.screens import BaseScreen
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp

# Load kv file
Builder.load_file('kv/splash_screen.kv')

class SplashScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)