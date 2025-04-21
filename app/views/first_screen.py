from app.views.screens import BaseScreen
from kivy.lang import Builder

# Load kv file
Builder.load_file('kv/first_screen.kv')

class FirstScreen(BaseScreen):
    def login_screen(self, *args):
        self.switch_screen('login_screen', 'left')
    
    def reg_screen(self, *args):
        self.switch_screen('reg_screen', 'left')