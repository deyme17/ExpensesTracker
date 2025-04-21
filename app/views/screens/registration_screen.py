# registration_screen.py
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
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Ellipse, RoundedRectangle, Line
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout

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
    required: False  # По умолчанию поле не обязательное
    
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
    
# Экран регистрации
<RegistrationScreen>:
    # Свойства для доступа из кода Python
    email_input: email_input
    password_input: password_input
    confirm_password_input: confirm_password_input
    name_input: name_input
    monobank_token_input: monobank_token_input
    error_label: error_label
    register_button: register_button
    
    # Фон
    AnimatedBackground:
        id: animated_bg
        size_hint: 1, 1
    
    # Скроллируемое содержимое
    ScrollView:
        size_hint: None, 0.9
        width: min(dp(350), root.width * 0.9)
        pos_hint: {'center_x': 0.5, 'center_y': 0.5}
        do_scroll_x: False
        do_scroll_y: True
        bar_width: dp(5)
        bar_color: primary_color
        bar_inactive_color: hint_color
        effect_cls: 'ScrollEffect'  # Плавный эффект скролла
        
        # Основной контейнер с эффектом карточки
        BoxLayout:
            orientation: 'vertical'
            size_hint: 1, None
            height: self.minimum_height
            padding: dp(25)
            spacing: dp(18)  # Отступ между элементами
            
            # Эффект карточки с тенью
            canvas.before:
                # Тень
                Color:
                    rgba: 0, 0, 0, 0.05
                RoundedRectangle:
                    pos: self.x - dp(5), self.y - dp(5)
                    size: self.width + dp(10), self.height + dp(10)
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
            
            # Заголовок с декоративной линией
            BoxLayout:
                orientation: 'vertical'
                size_hint_y: None
                height: dp(70)
                spacing: dp(5)
                
                Label:
                    text: 'Реєстрація'
                    font_size: '30sp'
                    color: text_light
                    bold: True
                    size_hint_y: None
                    height: dp(45)
                    
                # Декоративная линия
                Widget:
                    size_hint: None, None
                    size: dp(60), dp(3)
                    pos_hint: {'center_x': 0.5}
                    canvas:
                        Color:
                            rgba: primary_color
                        Rectangle:
                            pos: self.pos
                            size: self.size
            
            # Поля ввода - имя
            Label:
                text: "Ім'я"
                size_hint_y: None
                height: dp(30)
                color: text_light
                font_size: '16sp'
                halign: 'left'
                text_size: self.width, None
                
            FancyTextInput:
                id: name_input
                hint_text: "Введіть ім'я"
                size_hint_y: None
                height: dp(55)
                required: True
            
            # Поля ввода - email
            Label:
                text: "Email"
                size_hint_y: None
                height: dp(30)
                color: text_light
                font_size: '16sp'
                halign: 'left'
                text_size: self.width, None
                
            FancyTextInput:
                id: email_input
                hint_text: "Введіть email"
                size_hint_y: None
                height: dp(55)
                required: True
            
            # Поля ввода - пароль
            Label:
                text: "Пароль"
                size_hint_y: None
                height: dp(30)
                color: text_light
                font_size: '16sp'
                halign: 'left'
                text_size: self.width, None
                
            FancyTextInput:
                id: password_input
                hint_text: "Введіть пароль"
                password: True
                size_hint_y: None
                height: dp(55)
                required: True
            
            # Поля ввода - подтверждение пароля
            Label:
                text: "Підтвердження паролю"
                size_hint_y: None
                height: dp(30)
                color: text_light
                font_size: '16sp'
                halign: 'left'
                text_size: self.width, None
                
            FancyTextInput:
                id: confirm_password_input
                hint_text: "Введіть пароль ще раз"
                password: True
                size_hint_y: None
                height: dp(55)
                required: True
            
            # Разделитель
            Widget:
                size_hint_y: None
                height: dp(10)
            
            # Опциональный монобанк токен
            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: dp(30)
                
                Label:
                    text: "Монобанк токен (опціонально)"
                    size_hint_x: 0.8
                    color: text_light
                    font_size: '16sp'
                    halign: 'left'
                    text_size: self.width, None
                
                Button:
                    size_hint: None, None
                    size: dp(24), dp(24)
                    pos_hint: {'center_y': 0.5}
                    background_color: 0, 0, 0, 0
                    text: 'ℹ️'
                    font_size: '18sp'
                    on_press: root.show_token_info()
            
            FancyTextInput:
                id: monobank_token_input
                hint_text: "Введіть токен API MonoBank"
                size_hint_y: None
                height: dp(55)
                password: True  # Скрываем токен для безопасности
                required: False
                
            Label:
                text: "Токен використовується для автоматичного імпорту транзакцій"
                size_hint_y: None
                height: dp(30)
                color: hint_color
                font_size: '14sp'
                halign: 'left'
                text_size: self.width, None
            
            # Сообщение об ошибке
            Label:
                id: error_label
                text: root.error_message
                color: error_color
                font_size: '14sp'
                size_hint_y: None
                height: dp(30)
                opacity: root.show_error
            
            # Кнопка регистрации
            GlowButton:
                id: register_button
                text: 'Зареєструватись'
                size_hint_y: None
                height: dp(55)
                on_press: root.register()
            
            # Нижняя часть - ссылка на вход
            BoxLayout:
                orientation: 'horizontal'
                size_hint_y: None
                height: dp(40)
                padding: [0, dp(10), 0, 0]
                
                Label:
                    text: 'Вже маєте акаунт?'
                    font_size: '14sp'
                    color: hint_color
                    size_hint_x: 0.5
                    halign: 'right'
                    valign: 'middle'
                    text_size: self.size
                    padding_x: dp(5)
                
                Label:
                    text: 'Увійти'
                    font_size: '14sp'
                    color: accent_color
                    underline: True
                    size_hint_x: 0.5
                    halign: 'left'
                    valign: 'middle'
                    text_size: self.size
                    padding_x: dp(5)
                    on_touch_down: 
                        if self.collide_point(*args[1].pos): root.go_to_login()
''')

class RegistrationScreen(Screen):
    """Стильный экран регистрации с поддержкой MonoBank API"""
    # Свойства для связи с KV
    error_message = StringProperty("")
    show_error = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(RegistrationScreen, self).__init__(**kwargs)
        
        # Анимируем появление экрана
        self.opacity = 0
        Animation(opacity=1, d=0.8).start(self)
        
        # Запускаем анимацию фоновых частиц
        Clock.schedule_once(self._animate_particles, 0.5)
        
        # Создаем кнопку "Назад" и добавляем её на передний план (поверх всех элементов)
        self.back_button = Button(
            text='<',
            font_size='24sp',
            color=get_color_from_hex('#FFFFFF'),
            size_hint=(None, None),
            size=(dp(50), dp(50)),
            pos_hint={'x': 0.02, 'top': 0.98},
            background_color=(0, 0, 0, 0),
            on_release=self.go_back  # Используем on_release для более надежной работы
        )
        
        # Добавляем фон кнопки
        with self.back_button.canvas.before:
            Color(rgba=(1, 1, 1, 0.15))
            self.back_ellipse = Ellipse(pos=self.back_button.pos, size=self.back_button.size)
        
        # Привязываем обновление позиции и размера фона при изменении кнопки
        self.back_button.bind(pos=self.update_back_button, size=self.update_back_button)
        
        # Добавляем кнопку с небольшой задержкой, чтобы гарантировать, что она будет поверх всех элементов
        Clock.schedule_once(lambda dt: self.add_widget(self.back_button), 0.1)
    
    def update_back_button(self, instance, value):
        """Обновляет фон кнопки 'Назад' при изменении её размера или позиции"""
        if hasattr(self, 'back_ellipse'):
            self.back_ellipse.pos = instance.pos
            self.back_ellipse.size = instance.size
    
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
    
    def go_back(self, *args):
        """Возврат на стартовый экран"""
        print("Нажата кнопка назад")  # Для отладки
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'first_screen'
    
    def go_to_login(self, *args):
        """Переход на экран входа"""
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'auth_screen'
    
    def show_token_info(self, *args):
        """Показать информацию о MonoBank токене"""
        # Создаем модальное окно
        modal = ModalView(size_hint=(0.8, 0.5))
        
        # Создаем содержимое модального окна
        content = BoxLayout(orientation='vertical', padding=dp(20), spacing=dp(10))
        
        with content.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            RoundedRectangle(pos=content.pos, size=content.size, radius=[dp(10)])
        
        # Заголовок
        title = Label(
            text='Монобанк API Токен',
            font_size='20sp',
            bold=True,
            size_hint_y=None,
            height=dp(40),
            color=get_color_from_hex('#FFFFFF')
        )
        
        # Информация
        info = Label(
            text='Монобанк API токен дозволяє автоматично імпортувати ваші транзакції. '
                 'Ви можете отримати його в додатку Монобанк або на веб-сайті api.monobank.ua.\n\n'
                 'Ви можете додати свій токен пізніше в налаштуваннях програми.',
            font_size='16sp',
            halign='left',
            valign='top',
            size_hint_y=None,
            height=dp(150),
            text_size=(modal.width * 0.7, None),
            color=get_color_from_hex('#FFFFFF')
        )
        
        # Кнопка закрытия
        close_button = Button(
            text='Зрозуміло',
            size_hint=(None, None),
            size=(dp(150), dp(50)),
            pos_hint={'center_x': 0.5},
            background_color=get_color_from_hex('#FF7043')
        )
        close_button.bind(on_press=lambda x: modal.dismiss())
        
        # Добавляем виджеты в содержимое
        content.add_widget(title)
        content.add_widget(info)
        content.add_widget(close_button)
        
        # Добавляем содержимое в модальное окно
        modal.add_widget(content)
        
        # Показываем модальное окно
        modal.open()
    
    # Замените метод register в файле registration_screen.py на этот:

    def register(self, *args):
        """Обработка регистрации пользователя"""
        name = self.name_input.text.strip()
        email = self.email_input.text.strip()
        password = self.password_input.text
        confirm_password = self.confirm_password_input.text
        monobank_token = self.monobank_token_input.text.strip()
        
        # Валидация полей
        if not name:
            self.error_message = "Будь ласка, введіть ім'я"
            self._show_error()
            return
        
        if not email:
            self.error_message = "Будь ласка, введіть email"
            self._show_error()
            return
        
        # Проверка формата email
        if '@' not in email or '.' not in email:
            self.error_message = "Будь ласка, введіть коректний email"
            self._show_error()
            return
        
        if not password:
            self.error_message = "Будь ласка, введіть пароль"
            self._show_error()
            return
        
        if len(password) < 6:
            self.error_message = "Пароль має бути не менше 6 символів"
            self._show_error()
            return
        
        if password != confirm_password:
            self.error_message = "Паролі не співпадають"
            self._show_error()
            return
        
        # Эффект загрузки при регистрации
        self.register_button.text = "Реєстрація..."
        self.register_button.disabled = True
        
        # Имитация процесса регистрации
        def process_registration(dt):
            # Здесь должен быть реальный код регистрации
            # В демонстрационных целях регистрация всегда успешна
            success = True
            
            if success:
                # Переход на главный экран с транзакциями
                self.manager.transition = SlideTransition(direction='left')
                self.manager.current = 'main_screen'
            else:
                # Ошибка регистрации
                self.error_message = "Помилка при реєстрації. Спробуйте пізніше."
                self._show_error()
                self.register_button.text = "Зареєструватись"
                self.register_button.disabled = False
        
        # Имитируем задержку сети
        Clock.schedule_once(process_registration, 1.5)
    
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
    
    class TestRegistrationApp(App):
        def build(self):
            return RegistrationScreen()
    
    TestRegistrationApp().run()