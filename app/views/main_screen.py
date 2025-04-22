from app.views.screens import BaseScreen
from kivy.properties import StringProperty, NumericProperty, ListProperty, BooleanProperty, ObjectProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.uix.widget import Widget
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner, SpinnerOption
from kivy.graphics import Color, Rectangle, Ellipse, RoundedRectangle, Line, Mesh, Triangle
from datetime import datetime, timedelta
import calendar
import random

Builder.load_file('kv/main_screen.kv')

INCOME_CATEGORIES = ['Зарплата', 'Подарунок', 'Дивіденди', 'Фріланс', 'Відсотки', 'Інше']
EXPENSE_CATEGORIES = ['Продукти', 'Транспорт', 'Розваги', 'Здоровя', 'Одяг', 'Кафе', 'Звязок', 'Інше']
PAYMENT_METHODS = ['Всі', 'Картка', 'Готівка']

class MainScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        Clock.schedule_once(self._generate_sample_transactions, 0.2)
    
    def _generate_sample_transactions(self, dt):
        self.transactions_container.clear_widgets()
        now = datetime.now()

        for i in range(10):
            is_income = random.choice([True, False])
            category = random.choice(INCOME_CATEGORIES if is_income else EXPENSE_CATEGORIES)
            amount = random.randint(100, 10000) if is_income else -random.randint(100, 5000)
            days_ago = random.randint(0, 10)
            transaction_date = now - timedelta(days=days_ago)
            date_str = transaction_date.strftime("%d.%m.%Y")
            payment_method = random.choice(['Картка', 'Готівка'])
            transaction_row = Builder.load_string('''
TransactionRow:
    category: '{}'
    amount: '{:+,.0f}'
    date: '{}'
    is_income: {}
    payment_method: '{}'
'''.format(category, amount, date_str, is_income, payment_method))
            self.transactions_container.add_widget(transaction_row)

    def show_add_transaction(self, is_income=True):
        modal = ModalView(
            size_hint=(0.85, 0.65),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.7)
        )

        content = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=[dp(20), dp(20), dp(20), dp(20)],
            opacity=0
        )

        with content.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            self.content_rect = RoundedRectangle(size=content.size, pos=content.pos, radius=[dp(15)])
            color = get_color_from_hex('#66BB6A') if is_income else get_color_from_hex('#F44336')
            Color(rgba=color)
            RoundedRectangle(
                pos=(content.x + dp(15), content.y + content.height - dp(3)),
                size=(content.width - dp(30), dp(3)),
                radius=[dp(1.5)]
            )

        content.bind(size=self._update_rect, pos=self._update_rect)

        title_box = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        icon = BoxLayout(size_hint=(None, None), size=(dp(30), dp(30)))
        
        icon_color = get_color_from_hex('#66BB6A') if is_income else get_color_from_hex('#F44336')
        with icon.canvas:
            Color(rgba=icon_color)
            Ellipse(pos=icon.pos, size=icon.size)
            Color(rgba=get_color_from_hex('#FFFFFF'))
            Line(circle=(icon.center_x, icon.center_y, dp(13)), width=dp(2))
            Line(circle=(icon.center_x, icon.center_y, dp(7)), width=dp(1))
        
        def update_icon(instance, value):
            instance.canvas.clear()
            with instance.canvas:
                Color(rgba=icon_color)
                Ellipse(pos=instance.pos, size=instance.size)
                Color(rgba=get_color_from_hex('#FFFFFF'))
                Line(circle=(instance.center_x, instance.center_y, dp(13)), width=dp(2))
                Line(circle=(instance.center_x, instance.center_y, dp(7)), width=dp(1))
        
        icon.bind(pos=update_icon, size=update_icon)

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

        class StyledSpinner(Spinner):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.background_normal = ''
                self.background_down = ''
                self.bold = True
                self.color = get_color_from_hex('#0A4035')
                self.bind(size=self.update_background, pos=self.update_background)
                Clock.schedule_once(lambda dt: self.update_background(), 0)

            def update_background(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex('#D8F3EB'))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
                    Color(rgba=get_color_from_hex('#0A4035'))
                    x = self.x + self.width - dp(30)
                    y = self.y + self.height / 2 - dp(2)
                    Triangle(points=[
                        x, y + dp(5),
                        x + dp(10), y + dp(5),
                        x + dp(5), y - dp(5)
                    ])
        
        categories = INCOME_CATEGORIES if is_income else EXPENSE_CATEGORIES
        category_spinner = StyledSpinner(
            text=categories[0],
            values=categories,
            size_hint_y=None,
            height=dp(45),
            font_size=sp(16)
        )
        
        payment_spinner = StyledSpinner(
            text='Картка',
            values=['Картка', 'Готівка'],
            size_hint_y=None,
            height=dp(45),
            font_size=sp(16)
        )

        class StyledTextInput(TextInput):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.cursor_color = get_color_from_hex('#0A4035')
                self.foreground_color = get_color_from_hex('#0A4035')
                self.bold = True
                self.bind(size=self.update_background, pos=self.update_background)
                Clock.schedule_once(lambda dt: self.update_background(), 0)

            def update_background(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex('#D8F3EB'))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])

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

        description_input = StyledTextInput(
            hint_text='Додайте опис транзакції',
            hint_text_color=get_color_from_hex('#0A4035'),
            multiline=True,
            size_hint_y=None,
            height=dp(60),
            font_size=sp(16),
            padding=[dp(15), dp(12), dp(15), dp(12)]
        )

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

        class StyledButton(Button):
            def __init__(self, bg_color, **kwargs):
                super().__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.bg_color = bg_color
                self.color = get_color_from_hex('#FFFFFF')
                self.bind(size=self.update_background, pos=self.update_background)
                Clock.schedule_once(lambda dt: self.update_background(), 0)

            def update_background(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex(self.bg_color))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])

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
        cancel_button.bind(on_press=lambda x: modal.dismiss())
        save_button.bind(on_press=lambda x: self.save_transaction(
            category_spinner.text,
            amount_input.text,
            date_input.text,
            description_input.text,
            is_income,
            payment_spinner.text,
            modal
        ))

        buttons_box = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(15))
        buttons_box.add_widget(cancel_button)
        buttons_box.add_widget(save_button)

        content.add_widget(title_box)
        content.add_widget(Label(text='Категорія:', font_size=sp(16), color=get_color_from_hex('#FFFFFF'),
                                 halign='left', size_hint_y=None, height=dp(30), text_size=(None, dp(30))))
        content.add_widget(category_spinner)
        content.add_widget(Label(text='Тип оплати:', font_size=sp(16), color=get_color_from_hex('#FFFFFF'),
                                 halign='left', size_hint_y=None, height=dp(30), text_size=(None, dp(30))))
        content.add_widget(payment_spinner)
        content.add_widget(Label(text='Сума:', font_size=sp(16), color=get_color_from_hex('#FFFFFF'),
                                 halign='left', size_hint_y=None, height=dp(30), text_size=(None, dp(30))))
        content.add_widget(amount_input)
        content.add_widget(Label(text='Дата:', font_size=sp(16), color=get_color_from_hex('#FFFFFF'),
                                 halign='left', size_hint_y=None, height=dp(30), text_size=(None, dp(30))))
        content.add_widget(date_input)
        content.add_widget(Label(text='Опис:', font_size=sp(16), color=get_color_from_hex('#FFFFFF'),
                                 halign='left', size_hint_y=None, height=dp(30), text_size=(None, dp(30))))
        content.add_widget(description_input)
        content.add_widget(Widget())
        content.add_widget(buttons_box)

        modal.add_widget(content)
        modal.open()
        Animation(opacity=1, d=0.3).start(content)
    
    def _update_rect(self, instance, value):
        self.content_rect.pos = instance.pos
        self.content_rect.size = instance.size

    def show_add_transaction(self, is_income=True):
        modal = ModalView(
            size_hint=(0.9, 0.9),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.7)
        )

        content = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=[dp(20), dp(20), dp(20), dp(20)],
            opacity=0
        )

        with content.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            self.content_rect = RoundedRectangle(size=content.size, pos=content.pos, radius=[dp(15)])

        content.bind(size=self._update_rect, pos=self._update_rect)

        class CustomSpinner(Spinner):
            def __init__(self, **kwargs):
                super(CustomSpinner, self).__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.color = get_color_from_hex('#0A4035')
                self.bold = True
                self.font_size = sp(16)
                self.bind(pos=self.update_rect, size=self.update_rect)
                Clock.schedule_once(lambda dt: self.update_rect(), 0)
            
            def update_rect(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex('#FFFFFF'))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
                    Color(rgba=get_color_from_hex('#0A4035'))
                    x = self.x + self.width - dp(30)
                    y = self.y + self.height / 2 - dp(2)
                    Triangle(points=[
                        x, y + dp(5),
                        x + dp(10), y + dp(5),
                        x + dp(5), y - dp(5)
                    ])
        
        category_label = Label(
            text='Категорія:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        categories = INCOME_CATEGORIES if is_income else EXPENSE_CATEGORIES
        category_spinner = CustomSpinner(
            text=categories[0],
            values=categories,
            size_hint_y=None,
            height=dp(45)
        )

        payment_label = Label(
            text='Тип оплати:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        payment_spinner = CustomSpinner(
            text='Картка',
            values=['Картка', 'Готівка'],
            size_hint_y=None,
            height=dp(45)
        )

        amount_label = Label(
            text='Сума:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        class StyledTextInput(TextInput):
            def __init__(self, **kwargs):
                super(StyledTextInput, self).__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.cursor_color = get_color_from_hex('#0A4035')
                self.foreground_color = get_color_from_hex('#0A4035')
                self.font_size = sp(16)
                self.multiline = False
                self.padding = [dp(15), dp(10), dp(15), dp(10)]
                self.bind(pos=self.update_rect, size=self.update_rect)
                Clock.schedule_once(lambda dt: self.update_rect(), 0)
            
            def update_rect(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex('#FFFFFF'))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
        
        amount_input = StyledTextInput(
            hint_text='Введіть суму',
            hint_text_color=get_color_from_hex('#0A4035'),
            size_hint_y=None,
            height=dp(45)
        )

        currency_label = Label(
            text='Валюта:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        currency_spinner = CustomSpinner(
            text='UAH',
            values=['UAH', 'USD', 'EUR', 'PLN'],
            size_hint_y=None,
            height=dp(45)
        )

        date_label = Label(
            text='Дата:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        date_container = BoxLayout(
            orientation='horizontal',
            spacing=dp(5),
            size_hint_y=None,
            height=dp(45)
        )
        
        days = [str(i).zfill(2) for i in range(1, 32)]
        months = [str(i).zfill(2) for i in range(1, 13)]
        current_year = datetime.now().year
        years = [str(year) for year in range(current_year - 5, current_year + 1)]
        
        day_spinner = CustomSpinner(
            text=str(datetime.now().day).zfill(2),
            values=days,
            size_hint=(0.3, 1)
        )
        
        month_spinner = CustomSpinner(
            text=str(datetime.now().month).zfill(2),
            values=months,
            size_hint=(0.3, 1)
        )
        
        year_spinner = CustomSpinner(
            text=str(current_year),
            values=years,
            size_hint=(0.4, 1)
        )
        
        date_container.add_widget(day_spinner)
        date_container.add_widget(month_spinner)
        date_container.add_widget(year_spinner)

        cashback_label = Label(
            text='Кешбек:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        cashback_input = StyledTextInput(
            text='0',
            hint_text='Введіть відсоток кешбеку',
            hint_text_color=get_color_from_hex('#0A4035'),
            foreground_color=get_color_from_hex('#000000'),
            size_hint_y=None,
            height=dp(45)
        )

        commission_label = Label(
            text='Комісія:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        commission_input = StyledTextInput(
            text='0',
            hint_text='Введіть комісію',
            hint_text_color=get_color_from_hex('#0A4035'),
            foreground_color=get_color_from_hex('#000000'),
            size_hint_y=None,
            height=dp(45)
        )

        description_label = Label(
            text='Опис:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        description_input = StyledTextInput(
            hint_text='Додайте опис транзакції',
            hint_text_color=get_color_from_hex('#0A4035'),
            multiline=True,
            size_hint_y=None,
            height=dp(60)
        )
  
        description_input.multiline = True

        class StyledButton(Button):
            def __init__(self, bg_color, **kwargs):
                super(StyledButton, self).__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.bg_color = bg_color
                self.color = get_color_from_hex('#FFFFFF')
                self.bold = True
                self.bind(size=self.update_background, pos=self.update_background)
                Clock.schedule_once(lambda dt: self.update_background(), 0)

            def update_background(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex(self.bg_color))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])
        
        cancel_button = StyledButton(
            text='Скасувати',
            bg_color='#445555',
            size_hint_y=None,
            height=dp(50),
            font_size=sp(16)
        )
        
        save_button = StyledButton(
            text='Зберегти',
            bg_color='#0F7055',
            size_hint_y=None,
            height=dp(50),
            font_size=sp(16)
        )
        
        cancel_button.bind(on_press=lambda x: modal.dismiss())
        save_button.bind(on_press=lambda x: self.save_transaction(
            category_spinner.text,
            amount_input.text,
            f"{day_spinner.text}.{month_spinner.text}.{year_spinner.text}",
            description_input.text,
            is_income,
            payment_spinner.text,
            modal,
            currency_spinner.text,
            cashback_input.text,
            commission_input.text
        ))

        buttons_box = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(15))
        buttons_box.add_widget(cancel_button)
        buttons_box.add_widget(save_button)

        scroll_container = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            size_hint=(1, 1)
        )
        
        fields_container = BoxLayout(
            orientation='vertical', 
            spacing=dp(10),
            size_hint_y=None
        )
        fields_container.bind(minimum_height=fields_container.setter('height'))
        
        fields_container.add_widget(category_label)
        fields_container.add_widget(category_spinner)
        fields_container.add_widget(payment_label)
        fields_container.add_widget(payment_spinner)
        fields_container.add_widget(amount_label)
        fields_container.add_widget(amount_input)
        fields_container.add_widget(currency_label)
        fields_container.add_widget(currency_spinner)
        fields_container.add_widget(date_label)
        fields_container.add_widget(date_container)
        fields_container.add_widget(cashback_label)
        fields_container.add_widget(cashback_input)
        fields_container.add_widget(commission_label)
        fields_container.add_widget(commission_input)
        fields_container.add_widget(description_label)
        fields_container.add_widget(description_input)
        
        scroll_container.add_widget(fields_container)
        
        content.add_widget(scroll_container)
        content.add_widget(buttons_box)

        modal.add_widget(content)
        modal.open()
        Animation(opacity=1, d=0.3).start(content)

    def show_error_message(self, message):
        popup = Popup(
            title='Помилка',
            content=Label(text=message),
            size_hint=(0.7, 0.3),
            background='',
            background_color=(0, 0, 0, 0)
        )
        
        background_rect = RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(10)])
        error_bar = RoundedRectangle(
            pos=(popup.x + dp(10), popup.y + popup.height - dp(3)),
            size=(popup.width - dp(20), dp(3)),
            radius=[dp(1.5)]
        )
        
        with popup.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            background_rect
            Color(rgba=get_color_from_hex('#F44336'))
            error_bar
        
        def update_rects(instance, value):
            background_rect.pos = instance.pos
            background_rect.size = instance.size
            error_bar.pos = (instance.x + dp(10), instance.y + instance.height - dp(3))
            error_bar.size = (instance.width - dp(20), dp(3))
        
        popup.bind(pos=update_rects, size=update_rects)
        popup.title_color = get_color_from_hex('#FFFFFF')
        popup.title_size = sp(18)
        popup.content.color = get_color_from_hex('#FFFFFF')
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

    def go_statistics(self):
        self.switch_screen('statistics', 'left')

    def show_menu(self):
        popup = Popup(
            title='Меню',
            size_hint=(0.7, 0.3),
            background='',
            background_color=(0, 0, 0, 0)
        )
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(10)
        )
        
        background_rect = RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(10)])
        menu_bar = RoundedRectangle(
            pos=(popup.x + dp(10), popup.y + popup.height - dp(3)),
            size=(popup.width - dp(20), dp(3)),
            radius=[dp(1.5)]
        )
        
        with popup.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            background_rect
            Color(rgba=get_color_from_hex('#FF7043'))
            menu_bar
        
        def update_rects(instance, value):
            background_rect.pos = instance.pos
            background_rect.size = instance.size
            menu_bar.pos = (instance.x + dp(10), instance.y + instance.height - dp(3))
            menu_bar.size = (instance.width - dp(20), dp(3))
        
        popup.bind(pos=update_rects, size=update_rects)
        popup.title_color = get_color_from_hex('#FFFFFF')
        popup.title_size = sp(18)
        
        class MenuButton(Button):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.color = get_color_from_hex('#0A4035')
                self.font_size = sp(16)
                self.bind(size=self.update_bg, pos=self.update_bg)
                Clock.schedule_once(lambda dt: self.update_bg(), 0)
                
            def update_bg(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex('#D8F3EB'))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])

        logout_btn = MenuButton(
            text='Вийти з акаунту',
            size_hint_y=None,
            height=dp(45)
        )
        logout_btn.bind(on_press=lambda x: [popup.dismiss(), self.logout()])

        exit_btn = MenuButton(
            text='Вихід з додатку',
            size_hint_y=None,
            height=dp(45)
        )
        exit_btn.bind(on_press=lambda x: [popup.dismiss(), self.exit_app()])

        content.add_widget(logout_btn)
        content.add_widget(exit_btn)
        popup.content = content
        popup.open()    
        
    def logout(self):
        self.switch_screen('login_screen', 'right')

    def create_date_selector(self, is_start=True):
        box = BoxLayout(orientation='horizontal', spacing=dp(5), size_hint_y=None, height=dp(45))
        
        days = [str(i).zfill(2) for i in range(1, 32)]
        months = [str(i).zfill(2) for i in range(1, 13)]
        
        current_year = datetime.now().year
        years = [str(year) for year in range(current_year - 5, current_year + 1)]
        
        day_spinner = Spinner(
            text=days[0] if is_start else str(datetime.now().day).zfill(2),
            values=days,
            size_hint=(0.3, 1),
            background_color=get_color_from_hex('#FFF4E7'),
            color=get_color_from_hex('#0A4035'),
            font_size=sp(14)
        )
        
        month_spinner = Spinner(
            text=months[0] if is_start else str(datetime.now().month).zfill(2),
            values=months,
            size_hint=(0.3, 1),
            background_color=get_color_from_hex('#FFF4E7'),
            color=get_color_from_hex('#0A4035'),
            font_size=sp(14)
        )
        
        year_spinner = Spinner(
            text=str(current_year - 1) if is_start else str(current_year),
            values=years,
            size_hint=(0.4, 1),
            background_color=get_color_from_hex('#FFF4E7'),
            color=get_color_from_hex('#0A4035'),
            font_size=sp(14)
        )
        
        box.add_widget(day_spinner)
        box.add_widget(month_spinner)
        box.add_widget(year_spinner)
        
        return box, day_spinner, month_spinner, year_spinner

    def show_filter(self):
        modal = ModalView(
            size_hint=(0.9, 0.85),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.7)
        )

        content = BoxLayout(
            orientation='vertical',
            spacing=dp(12),
            padding=[dp(20), dp(20), dp(20), dp(20)],
            opacity=0
        )

        with content.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            self.content_rect = RoundedRectangle(size=content.size, pos=content.pos, radius=[dp(20)])
        
        content.bind(size=self._update_rect, pos=self._update_rect)

        title_label = Label(
            text='Фільтр транзакцій',
            font_size=sp(22),
            bold=True,
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            size_hint_y=None,
            height=dp(50)
        )

        class CustomSpinner(Spinner):
            def __init__(self, **kwargs):
                super(CustomSpinner, self).__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.color = get_color_from_hex('#0A4035')
                self.bold = True
                self.font_size = sp(16)
                self.bind(pos=self.update_rect, size=self.update_rect)
                Clock.schedule_once(lambda dt: self.update_rect(), 0)
            
            def update_rect(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex('#D8F3EB'))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
                    Color(rgba=get_color_from_hex('#0A4035'))
                    x = self.x + self.width - dp(30)
                    y = self.y + self.height / 2 - dp(2)
                    Triangle(points=[
                        x, y + dp(5),
                        x + dp(10), y + dp(5),
                        x + dp(5), y - dp(5)
                    ])

        class StyledTextInput(TextInput):
            def __init__(self, **kwargs):
                super(StyledTextInput, self).__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.cursor_color = get_color_from_hex('#0A4035')
                self.foreground_color = get_color_from_hex('#0A4035')
                self.font_size = sp(16)
                self.multiline = False
                self.padding = [dp(15), dp(10), dp(15), dp(10)]
                self.write_tab = False
                self.bind(pos=self.update_rect, size=self.update_rect)
                Clock.schedule_once(lambda dt: self.update_rect(), 0)
            
            def update_rect(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex('#D8F3EB'))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])

        sum_label = Label(
            text='Сума:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        amount_row = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(10))
        
        min_amount_box = BoxLayout(size_hint_x=0.5, spacing=dp(5))
        min_amount_label = Label(
            text="З:",
            size_hint=(None, 1),
            width=dp(20),
            color=get_color_from_hex('#FFFFFF'),
            font_size=sp(16)
        )
        min_amount = StyledTextInput(
            hint_text='0',
            text='0',
            hint_text_color=get_color_from_hex('#0A4035')
        )
        min_amount_box.add_widget(min_amount_label)
        min_amount_box.add_widget(min_amount)
        
        max_amount_box = BoxLayout(size_hint_x=0.5, spacing=dp(5))
        max_amount_label = Label(
            text="До:",
            size_hint=(None, 1),
            width=dp(25),
            color=get_color_from_hex('#FFFFFF'),
            font_size=sp(16)
        )
        max_amount = StyledTextInput(
            hint_text='1000000',
            text='1000000',
            hint_text_color=get_color_from_hex('#0A4035')
        )
        max_amount_box.add_widget(max_amount_label)
        max_amount_box.add_widget(max_amount)
        
        amount_row.add_widget(min_amount_box)
        amount_row.add_widget(max_amount_box)

        date_section = BoxLayout(
            orientation='vertical',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(140)
        )
        
        date_rect = RoundedRectangle(pos=date_section.pos, size=date_section.size, radius=[dp(12)])
        with date_section.canvas.before:
            Color(rgba=get_color_from_hex('#095045'))
            date_rect
        
        def update_date_rect(instance, value):
            date_rect.pos = instance.pos
            date_rect.size = instance.size
        
        date_section.bind(pos=update_date_rect, size=update_date_rect)
        
        date_title = Label(
            text="Інтервал дат:",
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        date_section.add_widget(date_title)
        
        days = [str(i).zfill(2) for i in range(1, 32)]
        months = [str(i).zfill(2) for i in range(1, 13)]
        
        current_year = datetime.now().year
        years = [str(year) for year in range(current_year - 5, current_year + 1)]
        
        date_from_row = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(4))
        date_from_label = Label(
            text="З:",
            size_hint=(None, 1),
            width=dp(20),
            color=get_color_from_hex('#FFFFFF'),
            font_size=sp(16)
        )
        date_from_row.add_widget(date_from_label)
        
        start_day_spinner = CustomSpinner(
            text='01',
            values=days,
            size_hint=(0.3, 1)
        )
        
        start_month_spinner = CustomSpinner(
            text='01',
            values=months,
            size_hint=(0.3, 1)
        )
        
        start_year_spinner = CustomSpinner(
            text=str(current_year - 1),
            values=years,
            size_hint=(0.4, 1)
        )
        
        date_from_row.add_widget(start_day_spinner)
        date_from_row.add_widget(start_month_spinner)
        date_from_row.add_widget(start_year_spinner)
        
        date_to_row = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(4))
  
        date_to_label = Label(
            text="До:",
            size_hint=(None, 1),
            width=dp(20),
            color=get_color_from_hex('#FFFFFF'),
            font_size=sp(16)
        )
        date_to_row.add_widget(date_to_label)
        
        end_day_spinner = CustomSpinner(
            text=str(datetime.now().day).zfill(2),
            values=days,
            size_hint=(0.3, 1)
        )
        
        end_month_spinner = CustomSpinner(
            text=str(datetime.now().month).zfill(2),
            values=months,
            size_hint=(0.3, 1)
        )
        
        end_year_spinner = CustomSpinner(
            text=str(current_year),
            values=years,
            size_hint=(0.4, 1)
        )
        
        date_to_row.add_widget(end_day_spinner)
        date_to_row.add_widget(end_month_spinner)
        date_to_row.add_widget(end_year_spinner)
        
        date_section.add_widget(date_from_row)
        date_section.add_widget(date_to_row)

        type_label = Label(
            text='Тип транзакції:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        type_spinner = CustomSpinner(
            text='Всі',
            values=['Всі', 'Доходи', 'Витрати'],
            size_hint_y=None,
            height=dp(45)
        )
        
        payment_label = Label(
            text='Спосіб оплати:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        payment_method_spinner = CustomSpinner(
            text='Всі',
            values=PAYMENT_METHODS,
            size_hint_y=None,
            height=dp(45)
        )

        class StyledButton(Button):
            def __init__(self, **kwargs):
                super(StyledButton, self).__init__(**kwargs)
                self.background_normal = ''
                self.background_down = ''
                self.background_color = (0, 0, 0, 0)
                self.color = get_color_from_hex('#0A4035')
                self.bold = True
                self.font_size = sp(16)
                self.bind(pos=self.update_rect, size=self.update_rect)
                Clock.schedule_once(lambda dt: self.update_rect(), 0)
            
            def update_rect(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex('#D8F3EB'))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])

        reset_button = StyledButton(text='Скинути')
        apply_button = StyledButton(text='Застосувати')

        reset_button.bind(on_press=lambda x: self.reset_filter(
            type_spinner, None, min_amount, max_amount,
            start_day_spinner, start_month_spinner, start_year_spinner,
            end_day_spinner, end_month_spinner, end_year_spinner,
            payment_method_spinner
        ))
        apply_button.bind(on_press=lambda x: self.apply_filter(
            type_spinner.text, None,
            min_amount.text, max_amount.text,
            f"{start_day_spinner.text}.{start_month_spinner.text}.{start_year_spinner.text}",
            f"{end_day_spinner.text}.{end_month_spinner.text}.{end_year_spinner.text}",
            payment_method_spinner.text,
            modal
        ))

        buttons_box = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(15))
        buttons_box.add_widget(reset_button)
        buttons_box.add_widget(apply_button)

        content.add_widget(title_label)
        content.add_widget(sum_label)
        content.add_widget(amount_row)
        content.add_widget(date_section)
        content.add_widget(type_label)
        content.add_widget(type_spinner)
        content.add_widget(payment_label)
        content.add_widget(payment_method_spinner)
        
        content.add_widget(Widget())
        content.add_widget(buttons_box)

        modal.add_widget(content)
        modal.open()
        Animation(opacity=1, d=0.3).start(content)
        
    def reset_filter(self, type_spinner, category_spinner, min_amount, max_amount, 
                    start_day_spinner, start_month_spinner, start_year_spinner,
                    end_day_spinner, end_month_spinner, end_year_spinner, payment_method_spinner):
        type_spinner.text = 'Всі'
        if category_spinner:
            category_spinner.text = 'Всі'
        payment_method_spinner.text = 'Всі'
        min_amount.text = '0'
        max_amount.text = '1000000'
        
        start_day_spinner.text = '01'
        start_month_spinner.text = '01'
        start_year_spinner.text = str(datetime.now().year - 1)
        
        end_day_spinner.text = str(datetime.now().day).zfill(2)
        end_month_spinner.text = str(datetime.now().month).zfill(2)
        end_year_spinner.text = str(datetime.now().year)

    def apply_filter(self, type_filter, category_filter, min_amount_text, max_amount_text, 
                     start_date, end_date, payment_method, modal):
        try:
            modal.dismiss()
            min_amount = float(min_amount_text.replace(',', '.')) if min_amount_text else 0
            max_amount = float(max_amount_text.replace(',', '.')) if max_amount_text else float('inf')

            try:
                start_day, start_month, start_year = start_date.split('.')
                start_date_obj = datetime(int(start_year), int(start_month), int(start_day))
            except:
                start_date_obj = datetime(datetime.now().year - 1, 1, 1)
                
            try:
                end_day, end_month, end_year = end_date.split('.')
                end_date_obj = datetime(int(end_year), int(end_month), int(end_day))
            except:
                end_date_obj = datetime.now()

            self.transactions_container.clear_widgets()
            now = datetime.now()

            for _ in range(15):
                if type_filter == 'Доходи':
                    is_income = True
                elif type_filter == 'Витрати':
                    is_income = False
                else:
                    is_income = random.choice([True, False])

                category = category_filter if category_filter != 'Всі' else random.choice(
                    INCOME_CATEGORIES if is_income else EXPENSE_CATEGORIES)
                    
                if payment_method == 'Картка':
                    current_payment = 'Картка'
                elif payment_method == 'Готівка':
                    current_payment = 'Готівка'
                else:
                    current_payment = random.choice(['Картка', 'Готівка'])

                amount = random.randint(100, 10000) if is_income else -random.randint(100, 5000)

                if min_amount is not None and abs(amount) < min_amount:
                    continue
                if max_amount is not None and abs(amount) > max_amount:
                    continue

                transaction_date = now - timedelta(days=random.randint(0, 100))
                if transaction_date < start_date_obj or transaction_date > end_date_obj:
                    continue

                date_str = transaction_date.strftime("%d.%m.%Y")

                transaction_row = Builder.load_string(f'''
TransactionRow:
    category: '{category}'
    amount: '{amount:+,.0f}'
    date: '{date_str}'
    is_income: {is_income}
    payment_method: '{current_payment}'
''')
                self.transactions_container.add_widget(transaction_row)

            self.show_success_message("Фільтр застосовано")

        except ValueError:
            self.show_error_message("Некоректне значення суми")
        except Exception as e:
            self.show_error_message(f"Помилка фільтрації: {str(e)}")

    def show_sort(self):
        modal = ModalView(
            size_hint=(0.8, 0.6),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.7)
        )

        content = BoxLayout(
            orientation='vertical',
            spacing=dp(12),
            padding=[dp(20), dp(20), dp(20), dp(20)],
            opacity=0
        )

        with content.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            self.content_rect = RoundedRectangle(size=content.size, pos=content.pos, radius=[dp(20)])
        
        content.bind(size=self._update_rect, pos=self._update_rect)

        title_label = Label(
            text='Сортування транзакцій',
            font_size=sp(22),
            bold=True,
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            size_hint_y=None,
            height=dp(50)
        )

        class CustomSpinner(Spinner):
            def __init__(self, **kwargs):
                super(CustomSpinner, self).__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.color = get_color_from_hex('#0A4035')
                self.bold = True
                self.font_size = sp(16)
                self.bind(pos=self.update_rect, size=self.update_rect)
                Clock.schedule_once(lambda dt: self.update_rect(), 0)
            
            def update_rect(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex('#D8F3EB'))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])
                    Color(rgba=get_color_from_hex('#0A4035'))
                    x = self.x + self.width - dp(30)
                    y = self.y + self.height / 2 - dp(2)
                    Triangle(points=[
                        x, y + dp(5),
                        x + dp(10), y + dp(5),
                        x + dp(5), y - dp(5)
                    ])

        field_label = Label(
            text='Сортувати за:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        sort_fields = ['Дата', 'Сума', 'Категорія', 'Тип оплати', 'Кешбек', 'Комісія']
        field_spinner = CustomSpinner(
            text=sort_fields[0],
            values=sort_fields,
            size_hint_y=None,
            height=dp(45)
        )
        
        direction_label = Label(
            text='Напрямок:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        direction_spinner = CustomSpinner(
            text='За зростанням',
            values=['За зростанням', 'За спаданням'],
            size_hint_y=None,
            height=dp(45)
        )

        class StyledButton(Button):
            def __init__(self, **kwargs):
                super(StyledButton, self).__init__(**kwargs)
                self.background_normal = ''
                self.background_down = ''
                self.background_color = (0, 0, 0, 0)
                self.color = get_color_from_hex('#0A4035')
                self.bold = True
                self.font_size = sp(16)
                self.bind(pos=self.update_rect, size=self.update_rect)
                Clock.schedule_once(lambda dt: self.update_rect(), 0)
            
            def update_rect(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex('#D8F3EB'))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(10)])

        cancel_button = StyledButton(text='Скасувати')
        apply_button = StyledButton(text='Застосувати')

        cancel_button.bind(on_press=lambda x: modal.dismiss())
        apply_button.bind(on_press=lambda x: self.apply_sort(
            field_spinner.text,
            direction_spinner.text == 'За зростанням',
            modal
        ))

        buttons_box = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(15))
        buttons_box.add_widget(cancel_button)
        buttons_box.add_widget(apply_button)

        content.add_widget(title_label)
        content.add_widget(field_label)
        content.add_widget(field_spinner)
        content.add_widget(direction_label)
        content.add_widget(direction_spinner)
        content.add_widget(Widget()) 
        content.add_widget(buttons_box)

        modal.add_widget(content)
        modal.open()
        Animation(opacity=1, d=0.3).start(content)

    def apply_sort(self, field, ascending, modal):
        modal.dismiss()
        
        # get all trnasactions
        transactions = list(self.transactions_container.children)
        
        # sort
        def sort_key(transaction):
            if field == 'Дата':
                date_str = transaction.date
                day, month, year = map(int, date_str.split('.'))
                return datetime(year, month, day)
            elif field == 'Сума':
                amount_str = transaction.amount.replace(',', '').replace(' ', '')
                return float(amount_str)
            elif field == 'Категорія':
                return transaction.category
            elif field == 'Тип оплати':
                return transaction.payment_method
            return ''
        
        # sort list
        sorted_transactions = sorted(transactions, key=sort_key, reverse=not ascending)
        
        self.transactions_container.clear_widgets()
        for transaction in sorted_transactions:
            self.transactions_container.add_widget(transaction)
        
        sort_direction = "за зростанням" if ascending else "за спаданням"
        self.show_success_message(f"Транзакції відсортовано за {field.lower()} {sort_direction}")

    def show_success_message(self, message):
        popup = Popup(
            title='Успіх',
            content=Label(text=message),
            size_hint=(0.7, 0.3),
            background='',
            background_color=(0, 0, 0, 0)
        )
        
        background_rect = RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(10)])
        success_bar = RoundedRectangle(
            pos=(popup.x + dp(10), popup.y + popup.height - dp(3)),
            size=(popup.width - dp(20), dp(3)),
            radius=[dp(1.5)]
        )
        
        with popup.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            background_rect
            Color(rgba=get_color_from_hex('#66BB6A'))
            success_bar
        
        def update_rects(instance, value):
            background_rect.pos = instance.pos
            background_rect.size = instance.size
            success_bar.pos = (instance.x + dp(10), instance.y + instance.height - dp(3))
            success_bar.size = (instance.width - dp(20), dp(3))
        
        popup.bind(pos=update_rects, size=update_rects)
        popup.title_color = get_color_from_hex('#FFFFFF')
        popup.title_size = sp(18)
        popup.content.color = get_color_from_hex('#FFFFFF')
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

    def exit_app(self):
        from kivy.core.window import Window
        Window.close()