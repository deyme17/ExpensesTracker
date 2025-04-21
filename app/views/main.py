# main.py - Головний файл додатку
from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition, FadeTransition
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.clock import Clock
# Імпортуємо наші екрани
from screens.splash_screen import SplashScreen
from screens.first_screen import FirstScreen
from screens.auth_screen import AuthScreen
from screens.registration_screen import RegistrationScreen
from screens.main_screen import MainScreen # Головний екран з транзакціями
from screens.stat_screen import StatisticsScreen # Екран статистики
# Налаштування додатку  

Window.size = (360, 640) # Розмір вікна для тестування
class ExpensesTrackerApp(App):
    """Головний додаток Expenses Tracker"""
    def build(self):
        # Створюємо менеджер екранів
        sm = ScreenManager(transition=FadeTransition())
        # Додаємо екрани
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(FirstScreen(name='first_screen'))
        sm.add_widget(AuthScreen(name='auth_screen'))
        sm.add_widget(RegistrationScreen(name='reg_screen'))
        sm.add_widget(MainScreen(name='main_screen'))
        sm.add_widget(StatisticsScreen(name='statistics')) # Додаємо екран статистики
        # Починаємо зі сплеш-екрану
        Clock.schedule_once(lambda dt: self.on_splash_complete(sm), 2.5)
        return sm
    
    def on_splash_complete(self, sm):
        """Перехід на стартовий екран після заставки"""
        sm.transition.direction = 'left'
        sm.current = 'first_screen'

if __name__ == '__main__':
    ExpensesTrackerApp().run()