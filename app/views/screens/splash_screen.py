# splash_screen.py
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.utils import get_color_from_hex
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp

# Загружаем KV файл
Builder.load_string('''
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import dp kivy.metrics.dp
#:import Animation kivy.animation.Animation

# Цветовая схема
#:set primary_color get_color_from_hex('#FF7043')      # Основной оранжевый
#:set secondary_color get_color_from_hex('#0F7055')    # Темно-зеленый
#:set bg_color get_color_from_hex('#062925')           # Фон (темно-зеленый)
#:set text_light get_color_from_hex('#FFFFFF')         # Светлый текст
#:set accent_color get_color_from_hex('#FFB74D')       # Светло-оранжевый

<SplashScreen>:
    canvas.before:
        Color:
            rgba: bg_color
        Rectangle:
            pos: self.pos
            size: self.size
            
        # Верхний градиент (тонкий акцент)
        Color:
            rgba: secondary_color[0], secondary_color[1], secondary_color[2], 0.2
        Ellipse:
            pos: self.center_x - self.width*0.75, -self.height*0.5
            size: self.width*1.5, self.height*1.0
            
        # Нижний градиент (тонкий акцент)
        Color:
            rgba: primary_color[0], primary_color[1], primary_color[2], 0.1
        Ellipse:
            pos: self.center_x - self.width*0.75, self.height*0.5
            size: self.width*1.5, self.height*1.0
    
    # Центральный блок с контентом (сохраняет пропорции)
    BoxLayout:
        orientation: 'vertical'
        spacing: dp(20)
        padding: dp(30)
        size_hint: None, None
        size: min(root.width * 0.8, dp(400)), min(root.height * 0.7, dp(500))
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        
        # Верхнее пространство
        Widget:
            size_hint_y: 0.1
    
        # Логотип с пульсацией
        Image:
            id: logo
            source: 'pictures/logo.png'
            size_hint: None, None
            size: dp(150), dp(150)
            pos_hint: {'center_x': 0.5}
            
            # Анимация пульсации
            on_kv_post:
                anim = Animation(size=(dp(160), dp(160)), duration=0.8, t='out_quad') + Animation(size=(dp(150), dp(150)), duration=0.8, t='in_quad')
                anim.repeat = True
                anim.start(self)
        
        # Небольшое пространство
        Widget:
            size_hint_y: 0.05
        
        # Название приложения
        Label:
            text: 'Expenses Tracker'
            font_size: '30sp'
            bold: True
            pos_hint: {'center_x': 0.5}
            color: text_light
            size_hint_y: None
            height: dp(50)
            opacity: 0
            
            on_kv_post:
                Animation(opacity=1, d=0.8).start(self)
        
        # Подзаголовок
        Label:
            text: 'Контролюйте свої фінанси'
            font_size: '16sp'
            pos_hint: {'center_x': 0.5}
            color: text_light
            opacity: 0.7
            size_hint_y: None
            height: dp(30)
            opacity: 0
            
            on_kv_post:
                Animation(opacity=0.7, d=1.0, t='out_quad').start(self)
                
        # Растягивающееся пространство
        Widget:
            size_hint_y: 0.2
        
        # Контейнер для индикатора загрузки (для лучшего позиционирования)
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            
            # Индикатор загрузки
            Widget:
                id: progress_bar
                size_hint: None, None
                size: dp(0), dp(4)
                pos_hint: {'center_x': 0.5}
                
                canvas:
                    Color:
                        rgba: primary_color
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(2)]
                
                on_kv_post:
                    anim = Animation(size=(dp(230), dp(4)), duration=1.5, t='out_quad')
                    anim.start(self)
            
            # Текст загрузки
            Label:
                text: 'Завантаження...'
                font_size: '14sp'
                color: accent_color
                opacity: 0
                size_hint_y: None
                height: dp(20)
                
                on_kv_post:
                    Animation(opacity=1, d=1.2).start(self)
        
        # Нижнее пространство
        Widget:
            size_hint_y: 0.1
''')

class SplashScreen(Screen):
    """Красивый экран загрузки приложения"""
    
    def __init__(self, **kwargs):
        super(SplashScreen, self).__init__(**kwargs)
        
        # Анимация появления
        self.opacity = 0
        Animation(opacity=1, d=0.3).start(self)
        
        # Запускаем анимацию фоновых частиц
        Clock.schedule_once(self._animate_particles, 0.5)
    
    def _animate_particles(self, dt):
        """Создает и анимирует декоративные частицы на фоне"""
        import random
        from kivy.uix.widget import Widget
        from kivy.graphics import Color, Ellipse
        
        # Создаем частицы
        for _ in range(15):
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
                alpha = random.uniform(0.1, 0.3)
                
                Color(r, g, b, alpha)
                Ellipse(pos=particle.pos, size=particle.size)
            
            self.add_widget(particle)
            
            # Анимируем частицу
            anim_duration = random.uniform(8, 20)
            anim_x = random.uniform(0, 1)
            anim_y = random.uniform(0, 1)
            
            anim = Animation(
                pos_hint={'x': anim_x, 'y': anim_y},
                duration=anim_duration
            )
            anim.repeat = True
            anim.start(particle)