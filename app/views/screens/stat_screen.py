# statistics_screen.py
from kivy.uix.screenmanager import Screen, SlideTransition
from kivy.properties import StringProperty, BooleanProperty, NumericProperty, ListProperty, ObjectProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.core.window import Window
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle, Ellipse, RoundedRectangle, Line

# Загружаем KV файл
Builder.load_string('''
#:import get_color_from_hex kivy.utils.get_color_from_hex
#:import SlideTransition kivy.uix.screenmanager.SlideTransition
#:import dp kivy.metrics.dp
#:import Clock kivy.clock.Clock
#:import Animation kivy.animation.Animation

# Цветовая схема (такая же как в auth_screen.py)
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
#:set income_color get_color_from_hex('#66BB6A')       # Зеленый для доходов
#:set expense_color get_color_from_hex('#F44336')      # Красный для расходов

# Стилизованная кнопка для типов графиков
<ChartButton@ToggleButton>:
    group: 'chart_type'
    background_color: 0, 0, 0, 0
    color: text_light if self.state == 'down' else hint_color
    font_size: '15sp'
    bold: self.state == 'down'
    allow_no_selection: False
    
    canvas.before:
        Color:
            rgba: primary_color if self.state == 'down' else (card_color[0]+0.1, card_color[1]+0.1, card_color[2]+0.1, 1)
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(8)]
        
        # Подсветка
        Color:
            rgba: accent_color if self.state == 'down' else (0, 0, 0, 0)
        Line:
            rounded_rectangle: [self.x, self.y, self.width, self.height, dp(8)]
            width: dp(1.5)
    
    # Эффект нажатия
    on_press: 
        self.background_color = 0, 0, 0, 0.1
        Animation(background_color=(0, 0, 0, 0), d=0.3).start(self)

# Стилизованная таблица
<StatsTable@GridLayout>:
    cols: 2
    padding: dp(10)
    spacing: dp(10)
    canvas.before:
        Color:
            rgba: card_color
        RoundedRectangle:
            pos: self.pos
            size: self.size
            radius: [dp(12)]
        
        # Легкая обводка
        Color:
            rgba: 1, 1, 1, 0.05
        Line:
            rounded_rectangle: [self.x, self.y, self.width, self.height, dp(12)]
            width: 1

# Анимированный фон (аналогично auth_screen)
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

# Главный экран статистики
<StatisticsScreen>:
    # Свойства для доступа из кода Python
    graph_container: graph_container
    histogram_btn: histogram_btn
    line_btn: line_btn
    pie_btn: pie_btn
    
    # Фон
    AnimatedBackground:
        id: animated_bg
        size_hint: 1, 1
    
    # Основной контейнер
    BoxLayout:
        orientation: 'vertical'
        padding: dp(10)
        spacing: dp(10)
        
        # Верхняя панель с заголовком и кнопкой меню
        BoxLayout:
            size_hint_y: None
            height: dp(60)
            padding: [dp(10), 0]
            
            # Иконка статистики
            BoxLayout:
                size_hint_x: None
                width: dp(50)
                canvas.before:
                    Color:
                        rgba: accent_color[0], accent_color[1], accent_color[2], 0.2
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(10)]
                
                Label:
                    text: '📊'
                    font_size: '24sp'
            
            # Текст заголовка
            Label:
                text: 'Статистика'
                color: text_light
                font_size: '24sp'
                bold: True
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                padding_x: dp(15)
                
            # Кнопка меню
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
        
        # Контейнер для графика
        BoxLayout:
            id: graph_container
            orientation: 'vertical'
            size_hint_y: 0.5
            
            canvas.before:
                Color:
                    rgba: card_color
                RoundedRectangle:
                    pos: self.pos
                    size: self.size
                    radius: [dp(12)]
                
                # Легкая обводка
                Color:
                    rgba: 1, 1, 1, 0.05
                Line:
                    rounded_rectangle: [self.x, self.y, self.width, self.height, dp(12)]
                    width: 1
        
        # Кнопки переключения типов графиков
        GridLayout:
            cols: 3
            size_hint_y: None
            height: dp(50)
            spacing: dp(10)
            padding: [dp(5), 0]
            
            ChartButton:
                id: histogram_btn
                text: 'Гістограма'
                state: 'down'
                on_release: root.change_chart_type('histogram')
                
            ChartButton:
                id: line_btn
                text: 'Лінійний'
                on_release: root.change_chart_type('line')
                
            ChartButton:
                id: pie_btn
                text: 'Кругова'
                on_release: root.change_chart_type('pie')
        
        # Таблица статистики
        StatsTable:
            size_hint_y: 0.3
            
            # Заголовки
            Label:
                text: 'Показник'
                color: hint_color
                font_size: '16sp'
                bold: True
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                
            Label:
                text: 'Значення'
                color: hint_color
                font_size: '16sp'
                bold: True
                text_size: self.size
                halign: 'right'
                valign: 'middle'
            
            # Среднее значение
            Label:
                text: 'Середнє значення'
                color: text_light
                font_size: '16sp'
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                
            Label:
                text: str(root.avg_value)
                color: primary_color
                font_size: '16sp'
                bold: True
                text_size: self.size
                halign: 'right'
                valign: 'middle'
            
            # Минимальное значение
            Label:
                text: 'Мінімальне'
                color: text_light
                font_size: '16sp'
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                
            Label:
                text: str(root.min_value)
                color: expense_color
                font_size: '16sp'
                bold: True
                text_size: self.size
                halign: 'right'
                valign: 'middle'
            
            # Максимальное значение
            Label:
                text: 'Максимальне'
                color: text_light
                font_size: '16sp'
                text_size: self.size
                halign: 'left'
                valign: 'middle'
                
            Label:
                text: str(root.max_value) 
                color: income_color
                font_size: '16sp'
                bold: True
                text_size: self.size
                halign: 'right'
                valign: 'middle'
        
        # Нижняя навигация - такой же стиль, как на main screen
        BoxLayout:
            size_hint_y: None
            height: dp(60)
            spacing: dp(5)
            
            # Кнопка "Транзакции"
            Button:
                text: 'Транзакції'
                background_color: 0, 0, 0, 0
                color: text_light
                
                canvas.before:
                    Color:
                        rgba: card_color
                    RoundedRectangle:
                        pos: self.pos
                        size: self.size
                        radius: [dp(10)]
                
                on_press: root.go_to_transactions()
            
            # Кнопка "Статистика"
            Button:
                text: 'Статистика'
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
''')

# Класс для рисования гистограммы
class HistogramWidget(Widget):
    def __init__(self, data=None, **kwargs):
        super(HistogramWidget, self).__init__(**kwargs)
        self.data = data or []
        self.bind(pos=self.update_canvas, size=self.update_canvas)
    
    def update_canvas(self, *args):
        self.canvas.clear()
        if not self.data:
            return
        
        with self.canvas:
            # Фоновый цвет
            Color(0.04, 0.25, 0.21, 1)  # Цвет фона графика
            Rectangle(pos=self.pos, size=self.size)
            
            # Координатные оси
            Color(0.7, 0.7, 0.7, 1)  # Серый цвет для осей
            Line(points=[self.x + dp(40), self.y + dp(20), 
                         self.x + dp(40), self.y + self.height - dp(20)])  # Ось Y
            Line(points=[self.x + dp(40), self.y + dp(20), 
                         self.x + self.width - dp(20), self.y + dp(20)])  # Ось X
            
            # Находим максимальное значение для масштабирования
            max_value = max([item['value'] for item in self.data])
            
            # Рисуем столбики гистограммы
            bar_width = (self.width - dp(70)) / len(self.data)
            
            for i, item in enumerate(self.data):
                # Вычисляем высоту столбика пропорционально значению
                bar_height = (item['value'] / max_value) * (self.height - dp(50))
                
                # Координаты столбика
                x1 = self.x + dp(50) + i * bar_width
                y1 = self.y + dp(20)
                
                # Рисуем столбик
                Color(*get_color_from_hex('#FF7043')[:3], 1)  # primary_color
                Rectangle(pos=(x1, y1), size=(bar_width * 0.7, bar_height))
                
                # Подпись на оси X
                label = Label(
                    text=item['name'],
                    size=(bar_width, dp(20)),
                    pos=(x1, self.y),
                    color=(0.8, 0.8, 0.8, 1),
                    font_size='10sp'
                )
                self.add_widget(label)
            
            # Добавляем метки на оси Y
            for i in range(5):
                # Значение метки
                value = int((i / 4) * max_value)
                y_pos = self.y + dp(20) + (i / 4) * (self.height - dp(50))
                
                # Горизонтальная линия сетки
                Color(0.5, 0.5, 0.5, 0.3)
                Line(points=[self.x + dp(40), y_pos, self.x + self.width - dp(20), y_pos])
                
                # Подпись значения
                label = Label(
                    text=str(value),
                    size=(dp(35), dp(20)),
                    pos=(self.x, y_pos - dp(10)),
                    color=(0.8, 0.8, 0.8, 1),
                    font_size='10sp'
                )
                self.add_widget(label)

# Класс для рисования линейного графика
class LineChartWidget(Widget):
    def __init__(self, data=None, **kwargs):
        super(LineChartWidget, self).__init__(**kwargs)
        self.data = data or []
        self.bind(pos=self.update_canvas, size=self.update_canvas)
    
    def update_canvas(self, *args):
        self.canvas.clear()
        if not self.data:
            return
        
        with self.canvas:
            # Фоновый цвет
            Color(0.04, 0.25, 0.21, 1)  # Цвет фона графика
            Rectangle(pos=self.pos, size=self.size)
            
            # Координатные оси
            Color(0.7, 0.7, 0.7, 1)  # Серый цвет для осей
            Line(points=[self.x + dp(40), self.y + dp(20), 
                         self.x + dp(40), self.y + self.height - dp(20)])  # Ось Y
            Line(points=[self.x + dp(40), self.y + dp(20), 
                         self.x + self.width - dp(20), self.y + dp(20)])  # Ось X
            
            # Находим максимальное значение для масштабирования
            max_value = max([item['value'] for item in self.data])
            
            # Подготавливаем точки для линии
            points = []
            x_step = (self.width - dp(70)) / (len(self.data) - 1) if len(self.data) > 1 else 0
            
            for i, item in enumerate(self.data):
                # Вычисляем координаты точки
                x = self.x + dp(50) + i * x_step
                y = self.y + dp(20) + (item['value'] / max_value) * (self.height - dp(50))
                points.extend([x, y])
                
                # Подпись на оси X
                label = Label(
                    text=item['name'],
                    size=(x_step, dp(20)),
                    pos=(x - x_step/2, self.y),
                    color=(0.8, 0.8, 0.8, 1),
                    font_size='10sp'
                )
                self.add_widget(label)
                
                # Точка на графике
                Color(*get_color_from_hex('#FFB74D')[:3], 1)  # accent_color
                Ellipse(pos=(x - dp(4), y - dp(4)), size=(dp(8), dp(8)))
            
            # Рисуем линию графика
            Color(*get_color_from_hex('#FFB74D')[:3], 1)  # accent_color
            Line(points=points, width=dp(2))
            
            # Добавляем метки на оси Y
            for i in range(5):
                # Значение метки
                value = int((i / 4) * max_value)
                y_pos = self.y + dp(20) + (i / 4) * (self.height - dp(50))
                
                # Горизонтальная линия сетки
                Color(0.5, 0.5, 0.5, 0.3)
                Line(points=[self.x + dp(40), y_pos, self.x + self.width - dp(20), y_pos])
                
                # Подпись значения
                label = Label(
                    text=str(value),
                    size=(dp(35), dp(20)),
                    pos=(self.x, y_pos - dp(10)),
                    color=(0.8, 0.8, 0.8, 1),
                    font_size='10sp'
                )
                self.add_widget(label)

# Класс для рисования круговой диаграммы
class PieChartWidget(Widget):
    def __init__(self, data=None, **kwargs):
        super(PieChartWidget, self).__init__(**kwargs)
        self.data = data or []
        self.bind(pos=self.update_canvas, size=self.update_canvas)
    
    def update_canvas(self, *args):
        self.canvas.clear()
        if not self.data:
            return
        
        # Удаляем все дочерние виджеты
        self.clear_widgets()
        
        with self.canvas:
            # Фоновый цвет
            Color(0.04, 0.25, 0.21, 1)  # Цвет фона графика
            Rectangle(pos=self.pos, size=self.size)
            
            # Вычисляем общую сумму для определения процентов
            total = sum([item['value'] for item in self.data])
            
            # Цвета для сегментов
            colors = [
                get_color_from_hex('#FF7043'),  # primary_color
                get_color_from_hex('#FFB74D'),  # accent_color
                get_color_from_hex('#66BB6A'),  # success_color
                get_color_from_hex('#42A5F5'),  # голубой
                get_color_from_hex('#EC407A'),  # розовый
                get_color_from_hex('#AB47BC')   # фиолетовый
            ]
            
            # Рисуем круговую диаграмму
            center_x = self.x + self.width * 0.35
            center_y = self.y + self.height * 0.5
            radius = min(self.width, self.height) * 0.35
            
            # Начальный угол (в градусах)
            start_angle = 0
            
            # Рисуем сегменты
            for i, item in enumerate(self.data):
                # Вычисляем угол для сегмента
                angle_size = item['value'] / total * 360
                
                # Рисуем сегмент
                Color(*colors[i % len(colors)][:3], 1)
                
                # Для круговой диаграммы используем сектор
                self._draw_sector(center_x, center_y, radius, start_angle, start_angle + angle_size)
                
                # Увеличиваем начальный угол для следующего сегмента
                start_angle += angle_size
            
            # Добавляем легенду
            legend_x = self.x + self.width * 0.65
            legend_y = self.y + self.height * 0.8
            
            for i, item in enumerate(self.data):
                # Рисуем цветной квадрат для легенды
                Color(*colors[i % len(colors)][:3], 1)
                Rectangle(pos=(legend_x, legend_y - i * dp(25)), size=(dp(15), dp(15)))
                
                # Добавляем текст
                percent = item['value'] / total * 100
                label = Label(
                    text=f"{item['name']}: {percent:.1f}%",
                    size=(dp(150), dp(20)),
                    pos=(legend_x + dp(20), legend_y - i * dp(25) - dp(10)),
                    color=(1, 1, 1, 1),
                    font_size='12sp',
                    halign='left',
                    text_size=(dp(150), dp(20))
                )
                self.add_widget(label)
    
    def _draw_sector(self, center_x, center_y, radius, start_angle, end_angle):
        """Рисует сектор круговой диаграммы"""
        from math import sin, cos, radians
        
        # Конвертируем углы в радианы
        start_rad = radians(start_angle)
        end_rad = radians(end_angle)
        
        # Точки для создания сектора
        points = [center_x, center_y]  # Начинаем с центра
        
        # Добавляем точку начала дуги
        points.extend([
            center_x + radius * cos(start_rad),
            center_y + radius * sin(start_rad)
        ])
        
        # Добавляем промежуточные точки для создания дуги
        # Чем больше точек, тем более гладкая дуга
        steps = max(1, int((end_angle - start_angle) / 5))  # Шаг в 5 градусов
        for i in range(1, steps + 1):
            angle = start_rad + (end_rad - start_rad) * i / steps
            points.extend([
                center_x + radius * cos(angle),
                center_y + radius * sin(angle)
            ])
        
        # Рисуем треугольный веер
        self.canvas.add(Color(1, 1, 1, 0.1))  # Светлое внутреннее заполнение
        mesh = self.canvas.add(Line(points=points, width=dp(2), joint='round', close=True))

class StatisticsScreen(Screen):
    """Экран статистики с анимированными графиками и статистикой транзакций"""
    # Свойства для связи с KV
    current_chart_type = StringProperty('histogram')
    avg_value = NumericProperty(0)
    min_value = NumericProperty(0)
    max_value = NumericProperty(0)
    
    def __init__(self, **kwargs):
        super(StatisticsScreen, self).__init__(**kwargs)
        self.name = 'statistics'
        self.chart_data = [
            {'name': 'Січ', 'value': 4000, 'month': 1},
            {'name': 'Лют', 'value': 3000, 'month': 2},
            {'name': 'Бер', 'value': 6000, 'month': 3},
            {'name': 'Кві', 'value': 8000, 'month': 4},
            {'name': 'Тра', 'value': 5000, 'month': 5},
            {'name': 'Чер', 'value': 7000, 'month': 6}
        ]
        
        # Рассчитываем статистические данные
        self._update_stats()
        
        # Выполняем анимацию при инициализации
        self.opacity = 0
        Animation(opacity=1, d=0.8).start(self)
        
        # Запускаем анимацию фоновых частиц
        Clock.schedule_once(self._animate_particles, 0.5)
    
    def on_enter(self):
        """Выполняется при переходе на экран"""
        # Обновляем график при каждом входе
        Clock.schedule_once(self._update_chart, 0.1)
    
    def _animate_particles(self, dt):
        """Создает декоративные частицы на фоне (как в auth_screen)"""
        import random
        
        # Создаем частицы
        for _ in range(15):
            particle = Widget(
                size_hint=(None, None),
                size=(dp(3), dp(3)),
                pos_hint={'x': random.random(), 'y': random.random()}
            )
            
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
    
    def change_chart_type(self, chart_type):
        """Меняет тип графика с анимацией"""
        if self.current_chart_type == chart_type:
            return
            
        self.current_chart_type = chart_type
        
        # Анимируем изменение графика
        self.graph_container.opacity = 0
        
        def update_and_show(dt):
            self._update_chart()
            Animation(opacity=1, d=0.5).start(self.graph_container)
            
        Clock.schedule_once(update_and_show, 0.3)
    
    def _update_chart(self, *args):
        """Обновляет текущий график"""
        # Очищаем контейнер
        self.graph_container.clear_widgets()
        
        if self.current_chart_type == 'histogram':
            chart = HistogramWidget(data=self.chart_data)
        elif self.current_chart_type == 'line':
            chart = LineChartWidget(data=self.chart_data)
        elif self.current_chart_type == 'pie':
            chart = PieChartWidget(data=self.chart_data)
        else:
            chart = Widget()  # Пустой виджет в случае ошибки
        
        self.graph_container.add_widget(chart)
    
    def _update_stats(self):
        """Обновляет статистические данные"""
        values = [item['value'] for item in self.chart_data]
        
        self.avg_value = sum(values) / len(values)
        self.min_value = min(values)
        self.max_value = max(values)
    
    def go_to_transactions(self):
        """Переход на экран транзакций"""
        self.manager.transition = SlideTransition(direction='right')
        self.manager.current = 'main_screen'
    
    def show_menu(self):
        """Показывает меню настроек только с функцией выхода"""
        popup = Popup(
            title='Меню',
            size_hint=(0.7, 0.2),
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
        
        # Только кнопка выхода
        exit_btn = Button(
            text='Вихід',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            size_hint_y=None,
            height=dp(45),
            font_size=sp(16)
        )
        exit_btn.bind(on_press=lambda x: [popup.dismiss(), self.exit_app()])
        content.add_widget(exit_btn)
        
        popup.content = content
        popup.open()
    
    def exit_app(self):
        """Выходит из приложения"""
        from kivy.app import App
        App.get_running_app().stop()

# Для тестирования отдельно
if __name__ == '__main__':
    from kivy.app import App
    
    class TestStatisticsApp(App):
        def build(self):
            return StatisticsScreen()
            
    TestStatisticsApp().run()