# auth_screen.py
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

# Цветовая схема
#:set primary_color get_color_from_hex('#FF7043')      # Основной оранжевый
#:set secondary_color get_color_from_hex('#0F7055')    # Темно-зеленый
#:set accent_color get_color_from_hex('#FFB74D')       # Светло-оранжевый
#:set bg_color get_color_from_hex('#062925')           # Фон (темно-зеленый)
#:set text_light get_color_from_hex('#FFFFFF')         # Светлый текст
#:set text_dark get_color_from_hex('#212121')          # Темный текст
#:set hint_color get_color_from_hex('#B0BEC5')         # Серый для подсказок
#:set card_color get_color_from_hex('#0A4035')         # Цвет карточки
#:set error_color get_color_from_hex('#F44336')        # Красный для ошибок
#:set success_color get_color_from_hex('#66BB6A')      # Зеленый для успеха

# Стилизованное текстовое поле
<FancyTextInput@TextInput>:
    background_color: 0, 0, 0, 0
    foreground_color: text_light
    hint_text_color: hint_color
    cursor_color: primary_color
    multiline: False
    padding: [dp(15), dp(12), dp(15), dp(10)]
    font_size: '16sp'
    
    canvas.before:
        Color:
            rgba: card_color[0]+0.05, card_color[1]+0.05, card_color[2]+0.05, 1
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(8)]
        
        # Нижняя линия для акцента
        Color:
            rgba: primary_color if self.focus else (hint_color[0], hint_color[1], hint_color[2], 0.5)
        Rectangle:
            pos: self.x + dp(10), self.y + dp(5)
            size: self.width - dp(20), dp(2) if self.focus else dp(1)

# Стилизованная кнопка с эффектами
<GlowButton@Button>:
    background_color: 0, 0, 0, 0
    color: text_light
    font_size: '18sp'
    bold: True
    
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
<AuthScreen>:
    # Свойства для доступа из кода Python
    email_input: email_input
    password_input: password_input
    error_label: error_label
    login_button: login_button
    
    # Фон
    AnimatedBackground:
        id: animated_bg
        size_hint: 1, 1
    
    # Кнопка "Назад"
    Button:
        text: '<'
        size_hint: None, None
        size: dp(44), dp(44)
        pos_hint: {'x': 0.03, 'top': 0.97}
        background_color: 0, 0, 0, 0
        on_press: root.go_back()
        
        canvas.before:
            Color:
                rgba: 1, 1, 1, 0.15
            Ellipse:
                pos: self.pos
                size: self.size
                
        Label:
            pos: self.parent.pos
            size: self.parent.size
            font_size: '24sp'
            color: text_light
    
    # Основной контейнер с эффектом карточки
    BoxLayout:
        orientation: 'vertical'
        size_hint: None, None
        size: dp(320), dp(450)  # Уменьшена высота 
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        padding: dp(25)
        spacing: dp(20)  # Увеличен отступ между элементами
        
        # Эффект карточки с тенью
        canvas.before:
            # Тень (многослойная для реалистичности)
            Color:
                rgba: 0, 0, 0, 0.05
            RoundedRectangle:
                pos: self.x - dp(5), self.y - dp(5)
                size: self.width + dp(10), self.height + dp(10)
                radius: [dp(20)]
                
            Color:
                rgba: 0, 0, 0, 0.03
            RoundedRectangle:
                pos: self.x - dp(10), self.y - dp(10)
                size: self.width + dp(20), self.height + dp(20)
                radius: [dp(20)]
                
            # Фон карточки
            Color:
                rgba: card_color
            RoundedRectangle:
                pos: self.pos
                size: self.size
                radius: [dp(20)]
                
            # Легкая обводка для 3D эффекта
            Color:
                rgba: 1, 1, 1, 0.05
            Line:
                rounded_rectangle: [self.x, self.y, self.width, self.height, dp(20)]
                width: 1
        
        # Логотип
        Image:
            source: 'pictures/logo.png'
            size_hint: None, None
            size: dp(120), dp(120)
            pos_hint: {'center_x': 0.5}
            allow_stretch: True
            keep_ratio: True
            opacity: 0  # Начальная прозрачность для анимации
            
            on_kv_post:
                Animation(opacity=1, d=1.0).start(self)
        
        # Заголовок с декоративной линией
        BoxLayout:
            orientation: 'vertical'
            size_hint_y: None
            height: dp(60)
            spacing: dp(5)
            
            Label:
                text: 'Авторизація'
                font_size: '28sp'
                color: text_light
                bold: True
                size_hint_y: None
                height: dp(40)
                
            # Декоративная линия
            Widget:
                size_hint: None, None
                size: dp(50), dp(3)
                pos_hint: {'center_x': 0.5}
                canvas:
                    Color:
                        rgba: primary_color
                    Rectangle:
                        pos: self.pos
                        size: self.size
        
        # Поля ввода
        FancyTextInput:
            id: email_input
            hint_text: 'Email'
            size_hint_y: None
            height: dp(60)
            
        FancyTextInput:
            id: password_input
            hint_text: 'Пароль'
            password: True
            size_hint_y: None
            height: dp(60)
        
        # Сообщение об ошибке
        Label:
            id: error_label
            text: root.error_message
            color: error_color
            font_size: '14sp'
            size_hint_y: None
            height: dp(30)
            opacity: root.show_error
        
        # Кнопка входа
        GlowButton:
            id: login_button
            text: 'Увійти'
            size_hint_y: None
            height: dp(50)
            on_press: root.login()
        
        # Опции "Забыли пароль" и "Регистрация"
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(30)
            spacing: dp(10)
            
            # Пустое пространство слева для баланса
            Widget:
                size_hint_x: 0.1
            
            # Забыли пароль    
            Label:
                text: 'Забули пароль?'
                font_size: '14sp'
                color: hint_color
                size_hint_x: 0.4
                halign: 'right'
                valign: 'middle'
                text_size: self.size
            
            # Регистрация    
            Label:
                text: 'Реєстрація'
                font_size: '14sp'
                color: accent_color
                underline: True
                size_hint_x: 0.4
                halign: 'left'
                valign: 'middle'
                text_size: self.size
                on_touch_down: 
                    if self.collide_point(*args[1].pos): root.go_to_registration()
                    
            # Пустое пространство справа для баланса    
            Widget:
                size_hint_x: 0.1
''')

class AuthScreen(Screen):
    """Стильный экран авторизации"""
    # Свойства для связи с KV
    error_message = StringProperty("")
    show_error = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(AuthScreen, self).__init__(**kwargs)
        
        # Анимируем появление экрана
        self.opacity = 0
        Animation(opacity=1, d=0.8).start(self)
        
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
    
    def go_back(self):
        """Возврат на стартовый экран"""
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'first_screen'
    
    def go_to_registration(self):
        """Переход на экран регистрации"""
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'reg_screen'
    
    def login(self):
        """Обработка авторизации с анимацией"""
        email = self.email_input.text
        password = self.password_input.text
        
        # Валидация полей
        if not email:
            self.error_message = "Будь ласка, введіть email"
            self._show_error()
            return
        
        if not password:
            self.error_message = "Будь ласка, введіть пароль"
            self._show_error()
            return
        
        # Эффект загрузки при авторизации
        self.login_button.text = "Авторизація..."
        self.login_button.disabled = True
    
    # Имитация процесса авторизации
        def authenticate(dt):
            # Здесь должен быть реальный код авторизации
            # В демонстрационных целях авторизация всегда успешна
            success = True
            if success:
                # Переход на главный экран с транзакциями
                self.manager.transition = SlideTransition(direction='left')
                self.manager.current = 'main_screen'
            else:
                # Ошибка авторизации
                self.error_message = "Невірний email або пароль"
                self._show_error()
                self.login_button.text = "Увійти"
                self.login_button.disabled = False

    # Имитируем задержку сети
        Clock.schedule_once(authenticate, 1)
    
    def _show_error(self):
        """Показывает сообщение об ошибке с анимацией"""
        # Сначала скрываем предыдущее сообщение
        if self.show_error > 0:
            Animation(show_error=0, duration=0.2).start(self)
            Clock.schedule_once(lambda dt: self._fade_in_error(), 0.3)
        else:
            self._fade_in_error()
    
    def _fade_in_error(self):
        """Плавное появление сообщения об ошибке"""
        Animation(show_error=1, duration=0.3).start(self)
        
        # Автоматически скрыть сообщение через 5 секунд
        Clock.schedule_once(
            lambda dt: Animation(show_error=0, duration=0.5).start(self), 
            5
        )

# Для тестирования отдельно
if __name__ == '__main__':
    from kivy.app import App
    
    class TestAuthApp(App):
        def build(self):
            return AuthScreen()
    
    TestAuthApp().run()