# first_screen.py
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import StringProperty, BooleanProperty, NumericProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle, Ellipse, RoundedRectangle, Line

# Загружаем KV файл
Builder.load_string('''
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import SlideTransition kivy.uix.screenmanager.SlideTransition
#:import dp kivy.metrics.dp
#:import Clock kivy.clock.Clock
#:import Animation kivy.animation.Animation

# Цветовая схема (такая же, как в auth_screen для единого стиля)
#:set primary_color get_color_from_hex('#FF7043')      # Основной оранжевый
#:set secondary_color get_color_from_hex('#0F7055')    # Темно-зеленый
#:set accent_color get_color_from_hex('#FFB74D')       # Светло-оранжевый
#:set bg_color get_color_from_hex('#062925')           # Фон (темно-зеленый)
#:set text_light get_color_from_hex('#FFFFFF')         # Светлый текст
#:set text_dark get_color_from_hex('#212121')          # Темный текст
#:set hint_color get_color_from_hex('#B0BEC5')         # Серый для подсказок
#:set card_color get_color_from_hex('#0A4035')         # Цвет карточки

# Стилизованная кнопка с эффектами
<WelcomeButton@Button>:
    background_color: 0, 0, 0, 0
    color: text_light
    font_size: '22sp'
    bold: True
    ripple_duration: 0.5
    ripple_scale: 1.05
    ripple_alpha_start: 0.4
    ripple_alpha_end: 0
    
    canvas.before:
        # Фон кнопки
        Color:
            rgba: primary_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(10)]
            
        # Эффект свечения
        Color:
            rgba: accent_color[0], accent_color[1], accent_color[2], 0.2
        RoundedRectangle:
            pos: self.x - dp(2), self.y - dp(2)
            size: self.width + dp(4), self.height + dp(4)
            radius: [dp(12)]
    
    # Эффект нажатия
    on_press: 
        self.background_color = 0, 0, 0, 0.1
        Animation(background_color=(0, 0, 0, 0), d=0.3).start(self)

# Animated Background
<AnimatedBackground@Widget>:
    canvas.before:
        Color:
            rgba: bg_color
        Rectangle:
            pos: self.pos
            size: self.size
        
        # Градиентный эффект
        Color:
            rgba: secondary_color[0], secondary_color[1], secondary_color[2], 0.15
        Ellipse:
            pos: self.center_x - self.width*0.75, self.center_y - self.height*0.75
            size: self.width*1.5, self.height*1.5

# Главный экран приложения
<FirstScreen>:
    # Фон
    AnimatedBackground:
        id: animated_bg
        size_hint: 1, 1

    # Основной контейнер
    FloatLayout:
        # Логотип с анимацией появления
        Image:
            id: logo
            source: 'pictures/logo.png'  # Исправлен путь
            size_hint: 0.7, 0.5
            pos_hint: {'center_x': 0.5, 'y': 0.62}
            opacity: 0  # Начальная прозрачность для анимации
            
            on_kv_post:
                Animation(opacity=1, d=1.0).start(self)
        
        # Заголовок с подсветкой
        Label:
            text: 'Expenses Tracker'
            font_size: '32sp'
            bold: True
            pos_hint: {'center_x': 0.5, 'center_y': 0.65}
            color: text_light
            opacity: 0  # Начальная прозрачность для анимации
            
            on_kv_post:
                Animation(opacity=1, d=1.2, t='out_back').start(self)
        
        # Декоративная линия под заголовком
        Widget:
            size_hint: None, None
            size: dp(200), dp(2)
            pos_hint: {'center_x': 0.5, 'center_y': 0.58}
            opacity: 0  # Начальная прозрачность для анимации
            
            canvas:
                Color:
                    rgba: primary_color
                Rectangle:
                    pos: self.pos
                    size: self.size
                    
            on_kv_post:
                Animation(opacity=1, d=1.4).start(self)
                
        # Кнопка регистрации
        WelcomeButton:
            text: 'Зареєструватись'
            size_hint: 0.75, None
            height: dp(60)
            pos_hint: {'center_x': 0.5, 'center_y': 0.45}
            opacity: 0  # Начальная прозрачность для анимации
            on_press: root.reg_screen()
            
            on_kv_post:
                Animation(opacity=1, pos_hint={'center_x': 0.5, 'center_y': 0.45}, d=0.8, t='out_back').start(self)
        
        # Кнопка входа
        WelcomeButton:
            text: 'Увійти'
            size_hint: 0.75, None
            height: dp(60)
            pos_hint: {'center_x': 0.5, 'center_y': 0.32}
            opacity: 0  # Начальная прозрачность для анимации
            on_press: root.auth_screen()
            
            on_kv_post:
                Animation(opacity=1, pos_hint={'center_x': 0.5, 'center_y': 0.32}, d=1.0, t='out_back').start(self)
                
        # Версия приложения
        Label:
            text: 'Version 1.0'
            font_size: '14sp'
            color: hint_color
            pos_hint: {'center_x': 0.5, 'y': 0.02}
            opacity: 0  # Начальная прозрачность для анимации
            
            on_kv_post:
                Animation(opacity=0.7, d=1.5).start(self)
''')

class FirstScreen(Screen):
    """Стильный стартовый экран с анимациями"""
    
    def __init__(self, **kwargs):
        super(FirstScreen, self).__init__(**kwargs)
        
        # Анимируем появление экрана
        self.opacity = 0
        Animation(opacity=1, d=0.5).start(self)
        
        # Запускаем анимацию фоновых частиц
        Clock.schedule_once(self._animate_particles, 0.5)
    
    def _animate_particles(self, dt):
        """Создает и анимирует декоративные частицы на фоне"""
        import random
        
        # Создаем частицы
        for _ in range(20):
            particle = Widget(
                size_hint=(None, None),
                size=(dp(3), dp(3)),
                pos_hint={'x': random.random(), 'y': random.random()}
            )
            
            # Добавляем графику частицы
            with particle.canvas:
                # Выбираем случайный цвет из палитры
                color_choice = random.choice([
                    get_color_from_hex('#FF7043'),  # Primary
                    get_color_from_hex('#FFB74D'),  # Accent
                    get_color_from_hex('#0F7055'),  # Secondary
                    get_color_from_hex('#FFFFFF')   # White
                ])
                
                # Добавляем прозрачность
                r, g, b = color_choice[0:3]
                alpha = random.uniform(0.1, 0.4)
                
                Color(r, g, b, alpha)
                Ellipse(pos=particle.pos, size=particle.size)
            
            self.add_widget(particle)
            
            # Анимируем частицу
            anim_duration = random.uniform(5, 15)
            anim_x = random.uniform(0, 1)
            anim_y = random.uniform(0, 1)
            
            anim = Animation(
                pos_hint={'x': anim_x, 'y': anim_y},
                duration=anim_duration
            )
            anim.repeat = True
            anim.start(particle)
    
    def auth_screen(self, *args):
        """Переход на экран авторизации"""
        # Добавляем анимацию перехода
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'auth_screen'
    
    def reg_screen(self, *args):
        """Переход на экран регистрации"""
        # Добавляем анимацию перехода
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'reg_screen'


# Код для тестирования (если файл запускается как основной)
if __name__ == '__main__':
    from kivy.app import App
    from kivy.uix.screenmanager import ScreenManager
    
    class TestApp(App):
        def build(self):
            sm = ScreenManager()
            sm.add_widget(FirstScreen(name='first_screen'))
            
            # Создаем заглушки для тестирования переходов
            auth = Screen(name='auth_screen')
            auth.add_widget(Label(text='Экран авторизации'))
            
            reg = Screen(name='reg_screen')
            reg.add_widget(Label(text='Экран регистрации'))
            
            sm.add_widget(auth)
            sm.add_widget(reg)
            
            return sm
    
    TestApp().run()