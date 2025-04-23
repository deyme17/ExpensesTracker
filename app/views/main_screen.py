from app.views.screens import BaseScreen
from kivy.properties import StringProperty, NumericProperty, ListProperty, BooleanProperty, ObjectProperty
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.metrics import dp, sp
from kivy.utils import get_color_from_hex
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle, Ellipse, RoundedRectangle, Line, Triangle
from datetime import datetime, timedelta
import random

# Load KV-файлу
Builder.load_file('kv/main_screen.kv')

INCOME_CATEGORIES = ['Зарплата', 'Подарунок', 'Дивіденди', 'Фріланс', 'Відсотки', 'Інше']
EXPENSE_CATEGORIES = ['Продукти', 'Транспорт', 'Розваги', 'Здоров’я', 'Одяг', 'Кафе', 'Зв’язок', 'Інше']
PAYMENT_METHODS = ['Всі', 'Картка', 'Готівка']

class SelectableTransactionRow(BoxLayout):
    category = StringProperty('')
    amount = StringProperty('')
    date = StringProperty('')
    is_income = BooleanProperty(False)
    payment_method = StringProperty('Картка')
    description = StringProperty('')
    currency = StringProperty('UAH')
    cashback = StringProperty('0')
    commission = StringProperty('0')
    transaction_id = StringProperty('')
    main_screen = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(SelectableTransactionRow, self).__init__(**kwargs)
        self.transaction_id = f"tr_{random.randint(10000, 99999)}"

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.main_screen.show_transaction_details(
                self.transaction_id, self.category, self.amount, self.date,
                self.is_income, self.payment_method, self.description,
                self.currency, self.cashback, self.commission
            )
            return True
        return super(SelectableTransactionRow, self).on_touch_down(touch)

class MainScreen(BaseScreen):
    def __init__(self, **kwargs):
        super(MainScreen, self).__init__(**kwargs)
        self.transaction_data = {}  
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
            description = f"Опис транзакції #{i+1}"
            currency = 'UAH'
            cashback = str(random.randint(0, 5))
            commission = str(random.randint(0, 2))

            transaction_row = SelectableTransactionRow(
                category=category,
                amount=f"{amount:+,.0f}",
                date=date_str,
                is_income=is_income,
                payment_method=payment_method,
                description=description,
                currency=currency,
                cashback=cashback,
                commission=commission,
                main_screen=self
            )

            self.transaction_data[transaction_row.transaction_id] = {
                'category': category,
                'amount': amount,
                'date': date_str,
                'is_income': is_income,
                'payment_method': payment_method,
                'description': description,
                'currency': currency,
                'cashback': cashback,
                'commission': commission
            }

            self.transactions_container.add_widget(transaction_row)

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

    def show_transaction_details(self, transaction_id, category, amount, date, is_income, payment_method, description, currency, cashback, commission):
        modal = ModalView(
            size_hint=(0.85, 0.75),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.6)
        )

        content = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=dp(20),
            opacity=0
        )

        with content.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            self.content_rect = RoundedRectangle(size=content.size, pos=content.pos, radius=[dp(15)])
        content.bind(size=self._update_rect, pos=self._update_rect)

        title = Label(
            text='Деталі транзакції',
            font_size=sp(20),
            bold=True,
            color=get_color_from_hex('#FFFFFF'),
            size_hint_y=None,
            height=dp(40),
            halign='center',
            valign='middle'
        )
        title.bind(size=lambda inst, val: setattr(inst, "text_size", (inst.width, None)))

        scroll_view = ScrollView(do_scroll_x=False)
        details = GridLayout(cols=1, spacing=dp(10), size_hint_y=None)
        details.bind(minimum_height=details.setter('height'))

        def add_row(label_text, value_text):
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30), spacing=dp(10))
            label = Label(
                text=f"{label_text}:",
                color=get_color_from_hex('#FFFFFF'),
                font_size=sp(16),
                size_hint_x=0.5,
                halign='left',
                valign='middle',
                text_size=(None, None)
            )
            value = Label(
                text=value_text,
                color=get_color_from_hex('#D8F3EB'),
                font_size=sp(16),
                size_hint_x=0.5, 
                halign='left',
                valign='middle',
                text_size=(None, None)
            )
            row.add_widget(label)
            row.add_widget(value)
            return row

        details.add_widget(add_row("Категорія", category))
        details.add_widget(add_row("Сума", f"{amount} {currency}"))
        details.add_widget(add_row("Дата", date))
        details.add_widget(add_row("Тип", "Дохід" if is_income else "Витрата"))
        details.add_widget(add_row("Тип оплати", payment_method))
        details.add_widget(add_row("Кешбек", cashback))
        details.add_widget(add_row("Комісія", commission))

        description_container = BoxLayout(
            orientation='vertical',
            spacing=dp(5),
            size_hint_y=None,
            height=dp(100)
        )

        description_label = Label(
            text='Опис:',
            color=get_color_from_hex('#FFFFFF'),
            font_size=sp(16),
            size_hint_x=0.5,
            halign='left',
            valign='middle',
            text_size=(None, None)
        )

        description_text = Label(
            text=description if description else "Опис відсутній",
            font_size=sp(14),
            color=get_color_from_hex('#D8F3EB'),
            halign='center', 
            valign='top',  
            size_hint_y=None,
            height=dp(70),
            text_size=(dp(300), dp(70)),  
            padding=(dp(10), dp(10))  
        )

        description_container.add_widget(description_label)
        description_container.add_widget(description_text)
        details.add_widget(description_container)

        scroll_view.add_widget(details)

        class StyledButton(Button):
            def __init__(self, bg_color, **kwargs):
                super().__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.bg_color = bg_color
                self.color = get_color_from_hex('#FFFFFF')
                self.bold = True
                self.font_size = sp(14)
                self.bind(size=self.update_background, pos=self.update_background)
                Clock.schedule_once(lambda dt: self.update_background(), 0)

            def update_background(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex(self.bg_color))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])

        buttons = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(15),
            padding=[dp(0), dp(5), dp(0), dp(0)]
        )
        
        edit_btn = StyledButton(text="Редагувати", bg_color="#0F7055", size_hint_x=0.33)
        delete_btn = StyledButton(text="Видалити", bg_color="#F44336", size_hint_x=0.33)
        close_btn = StyledButton(text="Закрити", bg_color="#445555", size_hint_x=0.33)

        edit_btn.bind(on_press=lambda x: [modal.dismiss(), self.edit_transaction(
            transaction_id, category, amount, date, is_income, payment_method,
            description, currency, cashback, commission)])
        delete_btn.bind(on_press=lambda x: [modal.dismiss(), self.confirm_delete_transaction([transaction_id])])
        close_btn.bind(on_press=lambda x: modal.dismiss())

        buttons.add_widget(edit_btn)
        buttons.add_widget(delete_btn)
        buttons.add_widget(close_btn)

        content.add_widget(title)
        content.add_widget(scroll_view)
        content.add_widget(buttons)

        modal.add_widget(content)
        modal.open()
        Animation(opacity=1, d=0.3).start(content)

    def confirm_delete_transaction(self, transaction_ids):
        if not transaction_ids:
            return

        modal = ModalView(
            size_hint=(0.8, 0.3),
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

        confirm_text = "Ви впевнені, що хочете видалити цю транзакцію?"
        confirm_label = Label(
            text=confirm_text,
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='center',
            valign='middle',
            size_hint_y=None,
            height=dp(60)
        )
        confirm_label.bind(
            size=lambda instance, value: setattr(instance, 'text_size', (instance.width, None))
        )

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
            height=dp(45),
            font_size=sp(16)
        )
        confirm_button = StyledButton(
            text='Видалити',
            bg_color='#F44336',
            size_hint_y=None,
            height=dp(45),
            font_size=sp(16)
        )

        cancel_button.bind(on_press=lambda x: modal.dismiss())
        confirm_button.bind(on_press=lambda x: [modal.dismiss(), self.delete_transactions(transaction_ids)])

        buttons_box = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(15))
        buttons_box.add_widget(cancel_button)
        buttons_box.add_widget(confirm_button)

        content.add_widget(confirm_label)
        content.add_widget(buttons_box)

        modal.add_widget(content)
        modal.open()
        Animation(opacity=1, d=0.3).start(content)

    def delete_transactions(self, transaction_ids):
        children_to_remove = []
        for child in self.transactions_container.children:
            if child.transaction_id in transaction_ids:
                children_to_remove.append(child)
                if child.transaction_id in self.transaction_data:
                    del self.transaction_data[child.transaction_id]

        for child in children_to_remove:
            self.transactions_container.remove_widget(child)

        self.show_success_message("Транзакцію видалено")

    def edit_transaction(self, transaction_id, category, amount, date, is_income, payment_method, description, currency, cashback, commission):
        amount_clean = amount.replace(',', '').replace('+', '').replace('-', '')
        day, month, year = date.split('.')

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
            text=category,
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
            text=payment_method,
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
            text=amount_clean,
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
            text=currency,
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
            text=day,
            values=days,
            size_hint=(0.3, 1)
        )

        month_spinner = CustomSpinner(
            text=month,
            values=months,
            size_hint=(0.3, 1)
        )

        year_spinner = CustomSpinner(
            text=year,
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
            text=cashback,
            hint_text='Введіть кешбек',
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
            text=commission,
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
            text=description,
            hint_text='Додайте опис транзакції',
            hint_text_color=get_color_from_hex('#0A4035'),
            multiline=True,
            size_hint_y=None,
            height=dp(60)
        )

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
            commission_input.text,
            edit_mode=True,
            transaction_id=transaction_id
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

    def save_transaction(self, category, amount_text, date, description, is_income, payment_method, modal,
                         currency='UAH', cashback='0', commission='0', edit_mode=False, transaction_id=None):
        try:
            amount = float(amount_text.replace(',', '.'))
            if amount <= 0:
                self.show_error_message("Сума має бути позитивним числом")
                return

            amount_display = f"+{amount:,.0f}" if is_income else f"-{amount:,.0f}"

            if edit_mode and transaction_id:
                for child in self.transactions_container.children:
                    if child.transaction_id == transaction_id:
                        child.category = category
                        child.amount = amount_display
                        child.date = date
                        child.is_income = is_income
                        child.payment_method = payment_method
                        child.description = description
                        child.currency = currency
                        child.cashback = cashback
                        child.commission = commission

                        self.transaction_data[transaction_id] = {
                            'category': category,
                            'amount': amount if is_income else -amount,
                            'date': date,
                            'is_income': is_income,
                            'payment_method': payment_method,
                            'description': description,
                            'currency': currency,
                            'cashback': cashback,
                            'commission': commission
                        }

                        modal.dismiss()
                        self.show_success_message("Транзакцію оновлено")
                        return

                self.show_error_message("Не вдалося знайти транзакцію для оновлення")
                return
            else:
                transaction_row = SelectableTransactionRow(
                    category=category,
                    amount=amount_display,
                    date=date,
                    is_income=is_income,
                    payment_method=payment_method,
                    description=description,
                    currency=currency,
                    cashback=cashback,
                    commission=commission,
                    main_screen=self
                )

                self.transaction_data[transaction_row.transaction_id] = {
                    'category': category,
                    'amount': amount if is_income else -amount,
                    'date': date,
                    'is_income': is_income,
                    'payment_method': payment_method,
                    'description': description,
                    'currency': currency,
                    'cashback': cashback,
                    'commission': commission
                }

                self.transactions_container.add_widget(transaction_row)
                modal.dismiss()
                self.show_success_message("Транзакцію додано")

        except ValueError:
            self.show_error_message("Некоректне значення суми. Введіть числове значення.")
        except Exception as e:
            self.show_error_message(f"Помилка: {str(e)}")

    def _update_rect(self, instance, value):
        self.content_rect.pos = instance.pos
        self.content_rect.size = instance.size

    def show_error_message(self, message):
        label = Label(
            text=message,
            color=get_color_from_hex('#FFFFFF'),
            font_size=sp(16),
            halign='center',
            valign='middle'
        )
        label.bind(size=label.setter('text_size'))

        popup = Popup(
            title='Помилка',
            content=label,
            size_hint=(0.7, 0.3),
            background='',
            background_color=(0, 0, 0, 0)
        )

        with popup.canvas.before:
            Color(rgba=get_color_from_hex('#8B0000'))
            background_rect = RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(10)])

        def update_rects(instance, value):
            background_rect.pos = instance.pos
            background_rect.size = instance.size

        popup.bind(pos=update_rects, size=update_rects)
        popup.open()
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

    def show_success_message(self, message):
        label = Label(
            text=message,
            color=get_color_from_hex('#FFFFFF'),
            font_size=sp(16),
            halign='center',
            valign='middle'
        )
        label.bind(size=label.setter('text_size'))

        popup = Popup(
            title='Успіх',
            content=label,
            size_hint=(0.7, 0.3),
            background='',
            background_color=(0, 0, 0, 0)
        )

        with popup.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            background_rect = RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(10)])

        def update_rects(instance, value):
            background_rect.pos = instance.pos
            background_rect.size = instance.size

        popup.bind(pos=update_rects, size=update_rects)
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

        popup.content = content

        with popup.canvas.before:
            color = Color(rgba=get_color_from_hex('#0A4035'))
            background_rect = RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(10)])

        def update_rects(instance, value):
            background_rect.pos = instance.pos
            background_rect.size = instance.size

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
            text='Вихід із програми',
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
                self.allow_copy = False
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

            filtered_transactions = []
            for transaction_id, data in self.transaction_data.items():
                amount = abs(data['amount'])
                transaction_date = datetime.strptime(data['date'], "%d.%m.%Y")

                if min_amount is not None and amount < min_amount:
                    continue
                if max_amount is not None and amount > max_amount:
                    continue
                if transaction_date < start_date_obj or transaction_date > end_date_obj:
                    continue
                if type_filter == 'Доходи' and not data['is_income']:
                    continue
                if type_filter == 'Витрати' and data['is_income']:
                    continue
                if payment_method != 'Всі' and data['payment_method'] != payment_method:
                    continue

                filtered_transactions.append(SelectableTransactionRow(
                    category=data['category'],
                    amount=f"{data['amount']:+,.0f}",
                    date=data['date'],
                    is_income=data['is_income'],
                    payment_method=data['payment_method'],
                    description=data['description'],
                    currency=data['currency'],
                    cashback=data['cashback'],
                    commission=data['commission'],
                    transaction_id=transaction_id,
                    main_screen=self
                ))

            self.transactions_container.clear_widgets()
            for transaction in filtered_transactions:
                self.transactions_container.add_widget(transaction)

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

        transactions = list(self.transactions_container.children)

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
            elif field == 'Кешбек':
                return float(transaction.cashback)
            elif field == 'Комісія':
                return float(transaction.commission)
            return ''

        sorted_transactions = sorted(transactions, key=sort_key, reverse=not ascending)

        self.transactions_container.clear_widgets()
        for transaction in sorted_transactions:
            self.transactions_container.add_widget(transaction)

        sort_direction = "за зростанням" if ascending else "за спаданням"
        self.show_success_message(f"Транзакції відсортовано за {field.lower()} {sort_direction}")

    def exit_app(self):
        from kivy.core.window import Window
        Window.close()