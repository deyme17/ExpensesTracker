from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, FadeTransition
from kivy.core.window import Window
from kivy.clock import Clock

from app.views.splash_screen import SplashScreen
from app.views.first_screen import FirstScreen
from app.views.login_screen import LoginScreen
from app.views.register_screen import RegistrationScreen
from app.views.main_screen import MainScreen 
from app.views.analytics_screen import AnalyticsScreen 

Window.size = (360, 640)

class ExpensesTrackerApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())

        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(FirstScreen(name='first_screen'))
        sm.add_widget(LoginScreen(name='login_screen'))
        sm.add_widget(RegistrationScreen(name='reg_screen'))
        sm.add_widget(MainScreen(name='main_screen'))
        sm.add_widget(AnalyticsScreen(name='statistics'))

        Clock.schedule_once(lambda dt: self.on_splash_complete(sm), 2.5)
        return sm
    
    def on_splash_complete(self, sm):
        sm.transition.direction = 'left'
        sm.current = 'first_screen'