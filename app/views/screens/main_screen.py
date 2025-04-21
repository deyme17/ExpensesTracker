# main_screen.py
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import StringProperty, NumericProperty, ListProperty, BooleanProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.graphics import Color, Rectangle, Ellipse, RoundedRectangle, Line, Mesh, Triangle
from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.popup import Popup
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from datetime import datetime, timedelta
import random

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
#:set card_light get_color_from_hex('#65F0C9')         # Светло-бирюзовый
#:set error_color get_color_from_hex('#F44336')        # Красный для ошибок
#:set success_color get_color_from_hex('#66BB6A')      # Зеленый для успеха
#:set light_bg get_color_from_hex('#D8F3EB')           # Светлый фон для таблицы

# Стилизованная кнопка
<CustomButton@Button>:
    background_color: 0, 0, 0, 0
    color: text_light
    font_size: '16sp'
    size_hint: None, None
    
    canvas.before:
        Color:
            rgba: light_bg
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(5)]

# Строка транзакции
<TransactionRow@BoxLayout>:
    category: ''
    amount: ''
    date: ''
    is_income: False
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(50)
    padding: dp(10)
    spacing: dp(5)
    
    canvas.before:
        Color:
            rgba: light_bg
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(5)]
            
    Label:
        text: root.category
        color: text_dark
        size_hint_x: 0.5
        text_size: self.size
        halign: 'left'
        valign: 'middle'
        
    Label:
        text: root.date
        color: hint_color
        size_hint_x: 0.25
        text_size: self.size
        halign: 'center'
        valign: 'middle'
        font_size: '14sp'
        
    Label:
        text: root.amount
        color: success_color if root.is_income else error_color
        size_hint_x: 0.25
        text_size: self.size
        halign: 'right'
        valign: 'middle'
        bold: True

# Главный экран приложения
<MainScreen>:
    transactions_container: transactions_container
    
    canvas.before:
        Color:
            rgba: bg_color
        Rectangle:
            pos: self.pos
            size: self.size
    
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        
        # Верхняя панель с балансом
        BoxLayout:
            size_hint_y: None
            height: dp(70)
            padding: dp(5)
            
            canvas.before:
                Color:
                    rgba: card_light
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(10)]
            
            # Иконка кошелька
            Widget:
                size_hint_x: None
                width: dp(50)
                
                canvas:
                    Color:
                        rgba: secondary_color
                    Line:
                        width: 1.5
                        rectangle: [self.x + dp(10), self.y + dp(15), dp(30), dp(20)]
                    Line:
                        width: 1.5
                        points: [self.x + dp(10), self.y + dp(35), self.x + dp(20), self.y + dp(45), self.x + dp(30), self.y + dp(45), self.x + dp(40), self.y + dp(35)]
                    
            # Баланс            
            Label:
                text: 'Баланс: 123456'
                font_size: '20sp'
                bold: True
                color: text_dark
                halign: 'left'
                valign: 'middle'
                text_size: self.size
                padding_x: dp(10)
            
            # Кнопка настроек  
            Button:
                size_hint: None, None
                size: dp(40), dp(40)
                pos_hint: {'center_y': 0.5}
                background_color: 0, 0, 0, 0
                on_press: root.show_menu()
                
                canvas.before:
                    Color:
                        rgba: secondary_color
                    Line:
                        width: 1.5
                        circle: (self.center_x, self.center_y, min(self.width, self.height) / 2 - dp(5), 0, 360)
                    Line:
                        width: 1.5
                        points: [self.center_x - dp(5), self.center_y - dp(2), self.center_x + dp(5), self.center_y - dp(2)]
                    Line:
                        width: 1.5
                        points: [self.center_x - dp(5), self.center_y + dp(2), self.center_x + dp(5), self.center_y + dp(2)]
        
        # Панель с кнопками выбора типа транзакции
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)

            # Кнопка дохода
            Button:
                text: 'Дохід'
                background_color: 0, 0, 0, 0
                color: text_light
                bold: True
                on_press: root.show_add_transaction(is_income=True)
                
                canvas.before:
                    Color:
                        rgba: success_color
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(10)]

            # Кнопка расхода
            Button:
                text: 'Витрати'
                background_color: 0, 0, 0, 0
                color: text_light
                bold: True
                on_press: root.show_add_transaction(is_income=False)
                
                canvas.before:
                    Color:
                        rgba: error_color
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(10)]
        
        # Заголовок секции транзакций
        BoxLayout:
            size_hint_y: None
            height: dp(50)
            padding: [dp(15), 0]
            
            canvas.before:
                Color:
                    rgba: card_color
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(10)]
            
            Label:
                text: 'Останні транзакції'
                font_size: '18sp'
                bold: True
                color: text_light
                halign: 'left'
                valign: 'middle'
                text_size: self.size
            
            # Кнопка фильтра
            Button:
                size_hint: None, None
                size: dp(40), dp(40)
                pos_hint: {'center_y': 0.5}
                background_color: 0, 0, 0, 0
                on_press: root.show_filter()
                
                canvas.before:
                    Color:
                        rgba: accent_color
                    Line:
                        width: 1.5
                        circle: (self.center_x, self.center_y, min(self.width, self.height) / 2 - dp(10), 0, 360)
                    Line:
                        width: 1.5
                        points: [self.center_x - dp(5), self.center_y, self.center_x + dp(5), self.center_y]
                    Line:
                        width: 1.5
                        points: [self.center_x, self.center_y - dp(5), self.center_x, self.center_y + dp(5)]
        
        # Таблица транзакций
        ScrollView:
            do_scroll_x: False
            do_scroll_y: True
            bar_width: dp(5)
            bar_color: primary_color
            bar_inactive_color: hint_color
            effect_cls: 'ScrollEffect'
            
            # Контейнер для транзакций
            GridLayout:
                id: transactions_container
                cols: 1
                spacing: dp(5)
                padding: dp(5)
                size_hint_y: None
                height: self.minimum_height
        
        # Нижняя навигация
        BoxLayout:
            size_hint_y: None
            height: dp(60)
            spacing: dp(5)
            
            # Кнопка "Транзакции"
            Button:
                text: 'Транзакції'
                background_color: 0, 0, 0, 0
                color: primary_color
                bold: True
                
                canvas.before:
                    Color:
                        rgba: card_color
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(10)]
                    
                    # Индикатор активного раздела
                    Color:
                        rgba: primary_color
                    Rectangle:
                        pos: self.x + dp(10), self.y + dp(5)
                        size: self.width - dp(20), dp(2)
            
            # Кнопка "Статистика"
            Button:
                text: 'Статистика'
                background_color: 0, 0, 0, 0
                color: text_light
                
                canvas.before:
                    Color:
                        rgba: card_color
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(10)]
                
                on_press: root.go_statistics()
''')

# Список категорий доходов и расходов на украинском языке
INCOME_CATEGORIES = ['Зарплата', 'Подарунок', 'Дивіденди', 'Фріланс', 'Відсотки', 'Інше']
EXPENSE_CATEGORIES = ['Продукти', 'Транспорт', 'Розваги', 'Здоровя', 'Одяг', 'Кафе', 'Звязок', 'Інше']

class MainScreen(Screen):
    """Главный экран с таблицей транзакций"""
    
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        
        # Анимируем появление экрана
        self.opacity = 0
        Animation(opacity=1, d=0.5).start(self)
        
        # Запускаем анимацию фоновых частиц
        Clock.schedule_once(self._animate_particles, 0.5)
        
        # Генерируем тестовые данные транзакций
        Clock.schedule_once(self._generate_sample_transactions, 0.2)
    
    def _animate_particles(self, dt):
        """Создает и анимирует декоративные частицы на фоне"""
        import random
        
        # Создаем меньше частиц для этого экрана
        for _ in range(10):
            particle = Widget(
                size_hint=(None, None),
                size=(dp(2), dp(2)),
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
                alpha = random.uniform(0.05, 0.2)  # Более прозрачные частицы
                
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
    
    def _generate_sample_transactions(self, dt):
        """Генерирует примеры транзакций для демонстрации"""
        self.transactions_container.clear_widgets()
        
        # Создаем несколько случайных транзакций
        now = datetime.now()
        
        # Транзакции за последние 10 дней
        for i in range(10):
            # Определяем, будет ли это доход или расход
            is_income = random.choice([True, False])
            
            # Выбираем случайную категорию
            category = random.choice(INCOME_CATEGORIES if is_income else EXPENSE_CATEGORIES)
            
            # Генерируем случайную сумму
            amount = random.randint(100, 10000) if is_income else -random.randint(100, 5000)
            
            # Генерируем случайную дату в прошлом
            days_ago = random.randint(0, 10)
            transaction_date = now - timedelta(days=days_ago)
            date_str = transaction_date.strftime("%d.%m.%Y")
            
            # Создаем строку транзакции
            transaction_row = Builder.load_string('''
TransactionRow:
    category: '{}'
    amount: '{:+,.0f}'
    date: '{}'
    is_income: {}
'''.format(category, amount, date_str, is_income))
            
            self.transactions_container.add_widget(transaction_row)

    def show_add_transaction(self, is_income=True):
        """Показывает окно для добавления новой транзакции с улучшенным дизайном"""
        # Создаем модальное окно с плавной анимацией
        modal = ModalView(
            size_hint=(0.85, 0.65),  # Увеличиваем размер для удобства ввода
            background='',  # Прозрачный фон для собственной отрисовки
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.7)  # Полупрозрачный фон оверлея
        )
        
        # Создаем контент
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=[dp(20), dp(20), dp(20), dp(20)],
            opacity=0  # Начинаем с прозрачного для анимации
        )
        
        # Добавляем фон и закругленные углы
        with content.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            self.content_rect = RoundedRectangle(size=content.size, pos=content.pos, radius=[dp(15)])
            
            # Стильная верхняя линия для дизайна - цвет зависит от типа транзакции
            color = get_color_from_hex('#66BB6A') if is_income else get_color_from_hex('#F44336')
            Color(rgba=color)
            RoundedRectangle(
                pos=(content.x + dp(15), content.y + content.height - dp(3)),
                size=(content.width - dp(30), dp(3)),
                radius=[dp(1.5)]
            )
        
        # Привязываем обновление размера и позиции фона при изменении контента
        content.bind(size=self._update_rect, pos=self._update_rect)
        
        # Заголовок с иконкой
        title_box = BoxLayout(
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )
        
        # Иконка (простой дизайн монеты)
        icon = BoxLayout(
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            padding=0
        )
        
        with icon.canvas:
            icon_color = get_color_from_hex('#66BB6A') if is_income else get_color_from_hex('#F44336')
            Color(rgba=icon_color)
            Ellipse(pos=icon.pos, size=icon.size)
            Color(rgba=get_color_from_hex('#FFFFFF'))
            Line(circle=(icon.center_x, icon.center_y, dp(13)), width=dp(2))
            Line(circle=(icon.center_x, icon.center_y, dp(7)), width=dp(1))
        
        # Заголовок
        title_text = 'Новий дохід' if is_income else 'Нова витрата'
        title = Label(
            text=title_text,
            font_size=sp(20),
            bold=True,
            color=get_color_from_hex('#FFFFFF'),
            halign='left'
        )
        
        title_box.add_widget(icon)
        title_box.add_widget(title)
        
        # Выбор категории
        category_label = Label(
            text='Категорія:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='left',
            size_hint_y=None,
            height=dp(30),
            text_size=(None, dp(30))
        )
        
        # Стилизуем выпадающий список
        class StyledSpinner(Spinner):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.background_normal = ''
                self.background_down = ''
                self.bold = True
                
                # Обновляем фон при изменении размера и позиции
                self.bind(size=self.update_background, pos=self.update_background)
                
            def update_background(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex('#D8F3EB'))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
                    
                    # Добавляем иконку "стрелка вниз"
                    Color(rgba=get_color_from_hex('#0A4035'))
                    x = self.x + self.width - dp(30)
                    y = self.y + self.height/2 - dp(2)
                    triangle_points = [
                        x, y + dp(5),
                        x + dp(10), y + dp(5),
                        x + dp(5), y - dp(5)
                    ]
                    Triangle(points=triangle_points)
        
        # Выбираем категории в зависимости от типа транзакции
        categories = INCOME_CATEGORIES if is_income else EXPENSE_CATEGORIES
        
        # Создаем стилизованный выпадающий список
        category_spinner = StyledSpinner(
            text=categories[0],
            values=categories,
            size_hint_y=None,
            height=dp(45),
            color=get_color_from_hex('#0A4035'),
            font_size=sp(16)
        )
        
        # Ввод суммы
        amount_label = Label(
            text='Сума:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='left',
            size_hint_y=None,
            height=dp(30),
            text_size=(None, dp(30))
        )
        
        # Стилизуем поле ввода
        class StyledTextInput(TextInput):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.cursor_color = get_color_from_hex('#0A4035')
                self.foreground_color = get_color_from_hex('#0A4035')
                self.bold = True
                
                # Обновляем фон при изменении размера и позиции
                self.bind(size=self.update_background, pos=self.update_background)
                
            def update_background(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex('#D8F3EB'))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
        
        # Создаем стилизованное поле ввода
        amount_input = StyledTextInput(
            hint_text='Введіть суму',
            hint_text_color=get_color_from_hex('#0A4035'),
            input_type='number',
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            font_size=sp(16),
            padding=[dp(15), dp(12), dp(15), dp(10)]
        )
        
        # Добавим поле для описания (опционально)
        description_label = Label(
            text='Опис (необов\'язково):',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='left',
            size_hint_y=None,
            height=dp(30),
            text_size=(None, dp(30))
        )
        
        description_input = StyledTextInput(
            hint_text='Додайте опис транзакції',
            hint_text_color=get_color_from_hex('#0A4035'),
            multiline=True,
            size_hint_y=None,
            height=dp(60),
            font_size=sp(16),
            padding=[dp(15), dp(12), dp(15), dp(12)]
        )
        
        # Поле для даты транзакции (по умолчанию текущая дата)
        date_label = Label(
            text='Дата:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='left',
            size_hint_y=None,
            height=dp(30),
            text_size=(None, dp(30))
        )
        
        # Получаем текущую дату
        current_date = datetime.now().strftime("%d.%m.%Y")
        
        date_input = StyledTextInput(
            text=current_date,
            hint_text='дд.мм.рррр',
            hint_text_color=get_color_from_hex('#0A4035'),
            multiline=False,
            size_hint_y=None,
            height=dp(45),
            font_size=sp(16),
            padding=[dp(15), dp(12), dp(15), dp(10)]
        )
        
        # Кнопки действий
        buttons_box = BoxLayout(
            size_hint_y=None,
            height=dp(45),
            spacing=dp(15)
        )
        
        # Стилизованные кнопки
        class StyledButton(Button):
            def __init__(self, bg_color, **kwargs):
                super().__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.bg_color = bg_color
                self.color = get_color_from_hex('#FFFFFF')
                
                # Обновляем фон при изменении размера и позиции
                self.bind(size=self.update_background, pos=self.update_background)
                
            def update_background(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex(self.bg_color))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
        
        # Создаем кнопки
        cancel_button = StyledButton(
            text='Скасувати',
            bg_color='#445555',
            font_size=sp(16),
            bold=True
        )
        
        save_button = StyledButton(
            text='Зберегти',
            bg_color='#0F7055',
            font_size=sp(16),
            bold=True
        )
        
        # Привязываем действия к кнопкам
        cancel_button.bind(on_press=lambda x: modal.dismiss())
        save_button.bind(on_press=lambda x: self.save_transaction(
            category_spinner.text,
            amount_input.text,
            date_input.text,
            description_input.text,
            is_income,
            modal
        ))
        
        # Добавляем кнопки в контейнер
        buttons_box.add_widget(cancel_button)
        buttons_box.add_widget(save_button)
        
        # Добавляем все элементы в контент
        content.add_widget(title_box)
        content.add_widget(category_label)
        content.add_widget(category_spinner)
        content.add_widget(amount_label)
        content.add_widget(amount_input)
        content.add_widget(date_label)
        content.add_widget(date_input)
        content.add_widget(description_label)
        content.add_widget(description_input)
        content.add_widget(Widget())  # Растягивающийся виджет для заполнения пустого пространства
        content.add_widget(buttons_box)
        
        # Добавляем контент в модальное окно
        modal.add_widget(content)
        
        # Анимируем появление модального окна
        modal.open()
        
        # Анимация контента
        Animation(opacity=1, d=0.3).start(content)
    
    def _update_rect(self, instance, value):
        """Обновляет прямоугольник фона при изменении размера или позиции"""
        self.content_rect.pos = instance.pos
        self.content_rect.size = instance.size
    
    def save_transaction(self, category, amount_text, date_text, description, is_income, modal):
        """Сохраняет транзакцию и обновляет список"""
        try:
            # Проверяем и конвертируем сумму
            if not amount_text:
                self.show_error_message("Будь ласка, введіть суму")
                return
                
            try:
                amount = float(amount_text.replace(',', '.'))
                if amount <= 0:
                    self.show_error_message("Сума повинна бути додатною")
                    return
            except ValueError:
                self.show_error_message("Некоректна сума")
                return
            
            # Проверяем дату
            if not date_text:
                self.show_error_message("Будь ласка, введіть дату")
                return
                
            try:
                # Пытаемся разобрать дату
                day, month, year = date_text.split('.')
                date_obj = datetime(int(year), int(month), int(day))
            except:
                self.show_error_message("Некоректний формат дати (дд.мм.рррр)")
                return
            
            # Закрываем модальное окно
            modal.dismiss()
            
            # Если все хорошо, добавляем транзакцию в список
            if not is_income:
                # Для расходов делаем сумму отрицательной
                amount = -amount
            
            # Форматируем дату
            date_str = date_obj.strftime("%d.%m.%Y")
            
            # Создаем строку транзакции и добавляем в начало списка
            transaction_row = Builder.load_string('''
TransactionRow:
    category: '{}'
    amount: '{:+,.0f}'
    date: '{}'
    is_income: {}
'''.format(category, amount, date_str, is_income))
            
            self.transactions_container.add_widget(transaction_row, index=0)
            
            # Показываем сообщение об успешном добавлении
            self.show_success_message("Транзакцію успішно додано")
            
        except Exception as e:
            self.show_error_message(f"Помилка: {str(e)}")
    
    def show_error_message(self, message):
        """Показывает сообщение об ошибке"""
        popup = Popup(
            title='Помилка',
            content=Label(text=message),
            size_hint=(0.7, 0.3),
            background='',
            background_color=(0, 0, 0, 0)
        )
        
        # Стилизуем попап
        with popup.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(10)])
            
            # Красная линия сверху для ошибки
            Color(rgba=get_color_from_hex('#F44336'))
            RoundedRectangle(
                pos=(popup.x + dp(10), popup.y + popup.height - dp(3)),
                size=(popup.width - dp(20), dp(3)),
                radius=[dp(1.5)]
            )
        
        popup.title_color = get_color_from_hex('#FFFFFF')
        popup.title_size = sp(18)
        popup.content.color = get_color_from_hex('#FFFFFF')
        
        popup.open()
        
        # Автоматически закрываем через 2 секунды
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)
    def go_statistics(self):
        self.manager.transition = SlideTransition(direction='left')
        self.manager.current = 'statistics'
    def show_menu(self):
        popup = Popup(
            title='Меню',
            size_hint=(0.7, 0.3),
            background='',
            background_color=(0, 0, 0, 0)
        )
        
        # Создаем контент
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(10)
        )
        
        # Стилизуем попап
        with popup.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(10)])
            
            # Оранжевая линия сверху
            Color(rgba=get_color_from_hex('#FF7043'))
            RoundedRectangle(
                pos=(popup.x + dp(10), popup.y + popup.height - dp(3)),
                size=(popup.width - dp(20), dp(3)),
                radius=[dp(1.5)]
            )
        
        popup.title_color = get_color_from_hex('#FFFFFF')
        popup.title_size = sp(18)
        
        # Кнопка выхода из аккаунта
        logout_btn = Button(
            text='Вийти з акаунту',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            size_hint_y=None,
            height=dp(45),
            font_size=sp(16)
        )
        logout_btn.bind(on_press=lambda x: [popup.dismiss(), self.logout()])
        
        # Кнопка выхода из приложения
        exit_btn = Button(
            text='Вихід з додатку',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            size_hint_y=None,
            height=dp(45),
            font_size=sp(16)
        )
        exit_btn.bind(on_press=lambda x: [popup.dismiss(), self.exit_app()])
        
        # Добавляем кнопки в контент
        content.add_widget(logout_btn)
        content.add_widget(exit_btn)
        
        popup.content = content
        popup.open()

    def logout(self):
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'auth_screen'

    def show_filter(self):
        # Создаем модальное окно с плавной анимацией
        modal = ModalView(
            size_hint=(0.85, 0.6),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.7)
        )
        
        # Создаем контент
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=[dp(20), dp(20), dp(20), dp(20)],
            opacity=0  # Начинаем с прозрачного для анимации
        )
        
        # Добавляем фон и закругленные углы
        with content.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            self.content_rect = RoundedRectangle(size=content.size, pos=content.pos, radius=[dp(15)])
            
            # Стильная верхняя линия для дизайна
            color = get_color_from_hex('#FFB74D')  # Акцентный цвет
            Color(rgba=color)
            RoundedRectangle(
                pos=(content.x + dp(15), content.y + content.height - dp(3)),
                size=(content.width - dp(30), dp(3)),
                radius=[dp(1.5)]
            )
        
        # Привязываем обновление размера и позиции фона при изменении контента
        content.bind(size=self._update_rect, pos=self._update_rect)
        
        # Заголовок с иконкой
        title_box = BoxLayout(
            size_hint_y=None,
            height=dp(40),
            spacing=dp(10)
        )
        
        # Иконка фильтра
        icon = BoxLayout(
            size_hint=(None, None),
            size=(dp(30), dp(30)),
            padding=0
        )
        
        with icon.canvas:
            Color(rgba=get_color_from_hex('#FFB74D'))
            # Рисуем простую иконку фильтра
            Line(points=[
                icon.center_x - dp(10), icon.center_y + dp(8),
                icon.center_x + dp(10), icon.center_y + dp(8)
            ], width=dp(2))
            Line(points=[
                icon.center_x - dp(5), icon.center_y,
                icon.center_x + dp(5), icon.center_y
            ], width=dp(2))
            Line(points=[
                icon.center_x, icon.center_y - dp(8),
                icon.center_x, icon.center_y - dp(8)
            ], width=dp(2))
        
        # Заголовок
        title = Label(
            text='Фільтр транзакцій',
            font_size=sp(20),
            bold=True,
            color=get_color_from_hex('#FFFFFF'),
            halign='left'
        )
        
        title_box.add_widget(icon)
        title_box.add_widget(title)
        
        # Фильтр по типу транзакции
        type_label = Label(
            text='Тип транзакції:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='left',
            size_hint_y=None,
            height=dp(30),
            text_size=(None, dp(30))
        )
        
        # Стилизуем выпадающий список
        class StyledSpinner(Spinner):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.background_normal = ''
                self.background_down = ''
                self.bold = True
                
                # Обновляем фон при изменении размера и позиции
                self.bind(size=self.update_background, pos=self.update_background)
                
            def update_background(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex('#D8F3EB'))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
                    
                    # Добавляем иконку "стрелка вниз"
                    Color(rgba=get_color_from_hex('#0A4035'))
                    x = self.x + self.width - dp(30)
                    y = self.y + self.height/2 - dp(2)
                    triangle_points = [
                        x, y + dp(5),
                        x + dp(10), y + dp(5),
                        x + dp(5), y - dp(5)
                    ]
                    Triangle(points=triangle_points)
        
        # Создаем стилизованный выпадающий список для типа транзакции
        type_spinner = StyledSpinner(
            text='Всі',
            values=['Всі', 'Доходи', 'Витрати'],
            size_hint_y=None,
            height=dp(45),
            color=get_color_from_hex('#0A4035'),
            font_size=sp(16)
        )
        
        # Фильтр по категории
        category_label = Label(
            text='Категорія:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='left',
            size_hint_y=None,
            height=dp(30),
            text_size=(None, dp(30))
        )
        
        # Объединяем все категории для списка
        all_categories = ['Всі'] + INCOME_CATEGORIES + EXPENSE_CATEGORIES
        
        # Создаем стилизованный выпадающий список для категорий
        category_spinner = StyledSpinner(
            text='Всі',
            values=all_categories,
            size_hint_y=None,
            height=dp(45),
            color=get_color_from_hex('#0A4035'),
            font_size=sp(16)
        )
        
        # Фильтр по дате
        date_label = Label(
            text='Період:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='left',
            size_hint_y=None,
            height=dp(30),
            text_size=(None, dp(30))
        )
        
        # Список периодов для фильтрации
        periods = ['Весь час', 'Сьогодні', 'Тиждень', 'Місяць', 'Рік']
        
        # Создаем стилизованный выпадающий список для периодов
        period_spinner = StyledSpinner(
            text='Весь час',
            values=periods,
            size_hint_y=None,
            height=dp(45),
            color=get_color_from_hex('#0A4035'),
            font_size=sp(16)
        )
        
        # Фильтр по сумме
        amount_label = Label(
            text='Сума:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='left',
            size_hint_y=None,
            height=dp(30),
            text_size=(None, dp(30))
        )
        
        # Стилизуем поле ввода
        class StyledTextInput(TextInput):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.cursor_color = get_color_from_hex('#0A4035')
                self.foreground_color = get_color_from_hex('#0A4035')
                self.bold = True
                
                # Обновляем фон при изменении размера и позиции
                self.bind(size=self.update_background, pos=self.update_background)
                
            def update_background(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex('#D8F3EB'))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
        
        # Контейнер для полей ввода суммы (от и до)
        amount_box = BoxLayout(
            size_hint_y=None,
            height=dp(45),
            spacing=dp(10)
        )
        
        # Поля для ввода минимальной и максимальной суммы
        min_amount = StyledTextInput(
            hint_text='Від',
            hint_text_color=get_color_from_hex('#0A4035'),
            input_type='number',
            multiline=False,
            font_size=sp(16),
            padding=[dp(15), dp(12), dp(15), dp(10)]
        )
        
        max_amount = StyledTextInput(
            hint_text='До',
            hint_text_color=get_color_from_hex('#0A4035'),
            input_type='number',
            multiline=False,
            font_size=sp(16),
            padding=[dp(15), dp(12), dp(15), dp(10)]
        )
        
        amount_box.add_widget(min_amount)
        amount_box.add_widget(max_amount)
        
        # Кнопки действий
        buttons_box = BoxLayout(
            size_hint_y=None,
            height=dp(45),
            spacing=dp(15)
        )
        
        # Стилизованные кнопки
        class StyledButton(Button):
            def __init__(self, bg_color, **kwargs):
                super().__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.bg_color = bg_color
                self.color = get_color_from_hex('#FFFFFF')
                
                # Обновляем фон при изменении размера и позиции
                self.bind(size=self.update_background, pos=self.update_background)
                
            def update_background(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex(self.bg_color))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
        
        # Создаем кнопки
        reset_button = StyledButton(
            text='Скинути',
            bg_color='#445555',
            font_size=sp(16),
            bold=True
        )
        
        apply_button = StyledButton(
            text='Застосувати',
            bg_color='#0F7055',
            font_size=sp(16),
            bold=True
        )
        
        # Привязываем действия к кнопкам
        reset_button.bind(on_press=lambda x: self.reset_filter(
            type_spinner, category_spinner, period_spinner, min_amount, max_amount
        ))
        apply_button.bind(on_press=lambda x: self.apply_filter(
            type_spinner.text, category_spinner.text, period_spinner.text, 
            min_amount.text, max_amount.text, modal
        ))
        
        # Добавляем кнопки в контейнер
        buttons_box.add_widget(reset_button)
        buttons_box.add_widget(apply_button)
        
        # Добавляем все элементы в контент
        content.add_widget(title_box)
        content.add_widget(type_label)
        content.add_widget(type_spinner)
        content.add_widget(category_label)
        content.add_widget(category_spinner)
        content.add_widget(date_label)
        content.add_widget(period_spinner)
        content.add_widget(amount_label)
        content.add_widget(amount_box)
        content.add_widget(Widget())  # Растягивающийся виджет для заполнения пустого пространства
        content.add_widget(buttons_box)
        
        # Добавляем контент в модальное окно
        modal.add_widget(content)
        
        # Анимируем появление модального окна
        modal.open()
        
        # Анимация контента
        Animation(opacity=1, d=0.3).start(content)

        def reset_filter(self, type_spinner, category_spinner, period_spinner, min_amount, max_amount):
            """Сбрасывает все настройки фильтра"""
            type_spinner.text = 'Всі'
            category_spinner.text = 'Всі'
            period_spinner.text = 'Весь час'
            min_amount.text = ''
            max_amount.text = ''

        def apply_filter(self, type_filter, category_filter, period_filter, min_amount_text, max_amount_text, modal):
            """Применяет фильтр к списку транзакций"""
            try:
                # Закрываем модальное окно
                modal.dismiss()
                
                # Подготавливаем параметры фильтра
                min_amount = None
                if min_amount_text:
                    try:
                        min_amount = float(min_amount_text.replace(',', '.'))
                    except ValueError:
                        self.show_error_message("Некоректна мінімальна сума")
                        return
                
                max_amount = None
                if max_amount_text:
                    try:
                        max_amount = float(max_amount_text.replace(',', '.'))
                    except ValueError:
                        self.show_error_message("Некоректна максимальна сума")
                        return
                
                # Применяем фильтрацию - для демонстрации просто регенерируем тестовые данные
                # В реальном приложении здесь должна быть логика фильтрации из базы данных
                self.transactions_container.clear_widgets()
                
                # Получаем текущую дату для фильтрации по периоду
                now = datetime.now()
                
                # Определяем границы периода
                if period_filter == 'Сьогодні':
                    date_from = now.replace(hour=0, minute=0, second=0, microsecond=0)
                elif period_filter == 'Тиждень':
                    date_from = now - timedelta(days=7)
                elif period_filter == 'Місяць':
                    date_from = now - timedelta(days=30)
                elif period_filter == 'Рік':
                    date_from = now - timedelta(days=365)
                else:  # 'Весь час'
                    date_from = now - timedelta(days=3650)  # ~10 лет назад
                
                # Создаем несколько транзакций (в реальном приложении здесь будет выборка из БД)
                for i in range(15):
                    # Определяем тип транзакции (доход/расход)
                    if type_filter == 'Доходи':
                        is_income = True
                    elif type_filter == 'Витрати':
                        is_income = False
                    else:  # 'Всі'
                        is_income = random.choice([True, False])
                    
                    # Выбираем категорию
                    if category_filter != 'Всі':
                        category = category_filter
                    else:
                        category = random.choice(INCOME_CATEGORIES if is_income else EXPENSE_CATEGORIES)
                    
                    # Генерируем сумму
                    if is_income:
                        amount = random.randint(100, 10000)
                    else:
                        amount = -random.randint(100, 5000)
                    
                    # Проверяем сумму на соответствие фильтру
                    if min_amount is not None and amount < min_amount:
                        continue
                    if max_amount is not None and amount > max_amount:
                        continue
                    
                    # Генерируем дату
                    days_ago = random.randint(0, 100)  # За последние 100 дней
                    transaction_date = now - timedelta(days=days_ago)
                    
                    # Проверяем дату на соответствие периоду
                    if transaction_date < date_from:
                        continue
                    
                    date_str = transaction_date.strftime("%d.%m.%Y")
                    
                    # Создаем строку транзакции
                    transaction_row = Builder.load_string('''
        TransactionRow:
            category: '{}'
            amount: '{:+,.0f}'
            date: '{}'
            is_income: {}
        '''.format(category, amount, date_str, is_income))
                    
                    self.transactions_container.add_widget(transaction_row)
                
                # Показываем сообщение об успешной фильтрации
                self.show_success_message("Фільтр застосовано")
                
            except Exception as e:
                self.show_error_message(f"Помилка фільтрації: {str(e)}")

        def show_success_message(self, message):
            """Показывает сообщение об успехе"""
            popup = Popup(
                title='Успіх',
                content=Label(text=message),
                size_hint=(0.7, 0.3),
                background='',
                background_color=(0, 0, 0, 0)
            )
            
            # Стилизуем попап
            with popup.canvas.before:
                Color(rgba=get_color_from_hex('#0A4035'))
                RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(10)])
                
                # Зеленая линия сверху для успеха
                Color(rgba=get_color_from_hex('#66BB6A'))
                RoundedRectangle(
                    pos=(popup.x + dp(10), popup.y + popup.height - dp(3)),
                    size=(popup.width - dp(20), dp(3)),
                    radius=[dp(1.5)]
                )
            
            popup.title_color = get_color_from_hex('#FFFFFF')
            popup.title_size = sp(18)
            popup.content.color = get_color_from_hex('#FFFFFF')
            
            popup.open()
            
            # Автоматически закрываем через 2 секунды
            Clock.schedule_once(lambda dt: popup.dismiss(), 2)

        def exit_app(self):
            """Выход из приложения"""
            from kivy.core.window import Window
            Window.close()