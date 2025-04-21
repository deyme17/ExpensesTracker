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
from kivy.uix.modalview import ModalView
from kivy.uix.textinput import TextInput
from kivy.uix.spinner import Spinner
from kivy.graphics import Color, Rectangle, Ellipse, RoundedRectangle, Line, Mesh, Triangle
from datetime import datetime, timedelta
import random

# Load kv file
Builder.load_file('kv/main_screen.kv')

INCOME_CATEGORIES = ['Зарплата', 'Подарунок', 'Дивіденди', 'Фріланс', 'Відсотки', 'Інше']
EXPENSE_CATEGORIES = ['Продукти', 'Транспорт', 'Розваги', 'Здоровя', 'Одяг', 'Кафе', 'Звязок', 'Інше']

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
            transaction_row = Builder.load_string('''
TransactionRow:
    category: '{}'
    amount: '{:+,.0f}'
    date: '{}'
    is_income: {}
'''.format(category, amount, date_str, is_income))
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
        with icon.canvas:
            icon_color = get_color_from_hex('#66BB6A') if is_income else get_color_from_hex('#F44336')
            Color(rgba=icon_color)
            Ellipse(pos=icon.pos, size=icon.size)
            Color(rgba=get_color_from_hex('#FFFFFF'))
            Line(circle=(icon.center_x, icon.center_y, dp(13)), width=dp(2))
            Line(circle=(icon.center_x, icon.center_y, dp(7)), width=dp(1))

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
                self.bind(size=self.update_background, pos=self.update_background)

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
            color=get_color_from_hex('#0A4035'),
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
            modal
        ))

        buttons_box = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(15))
        buttons_box.add_widget(cancel_button)
        buttons_box.add_widget(save_button)

        content.add_widget(title_box)
        content.add_widget(Label(text='Категорія:', font_size=sp(16), color=get_color_from_hex('#FFFFFF'),
                                 halign='left', size_hint_y=None, height=dp(30), text_size=(None, dp(30))))
        content.add_widget(category_spinner)
        content.add_widget(Label(text='Сума:', font_size=sp(16), color=get_color_from_hex('#FFFFFF'),
                                 halign='left', size_hint_y=None, height=dp(30), text_size=(None, dp(30))))
        content.add_widget(amount_input)
        content.add_widget(Label(text='Дата:', font_size=sp(16), color=get_color_from_hex('#FFFFFF'),
                                 halign='left', size_hint_y=None, height=dp(30), text_size=(None, dp(30))))
        content.add_widget(date_input)
        content.add_widget(Label(text='Опис (необов\'язково):', font_size=sp(16), color=get_color_from_hex('#FFFFFF'),
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

    def save_transaction(self, category, amount_text, date_text, description, is_income, modal):
        try:
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

            if not date_text:
                self.show_error_message("Будь ласка, введіть дату")
                return

            try:
                day, month, year = date_text.split('.')
                date_obj = datetime(int(year), int(month), int(day))
            except:
                self.show_error_message("Некоректний формат дати (дд.мм.рррр)")
                return

            modal.dismiss()

            if not is_income:
                amount = -amount

            date_str = date_obj.strftime("%d.%m.%Y")
            transaction_row = Builder.load_string('''
TransactionRow:
    category: '{}'
    amount: '{:+,.0f}'
    date: '{}'
    is_income: {}
'''.format(category, amount, date_str, is_income))

            self.transactions_container.add_widget(transaction_row, index=0)
            self.show_success_message("Транзакцію успішно додано")

        except Exception as e:
            self.show_error_message(f"Помилка: {str(e)}")

    def show_error_message(self, message):
        popup = Popup(
            title='Помилка',
            content=Label(text=message),
            size_hint=(0.7, 0.3),
            background='',
            background_color=(0, 0, 0, 0)
        )
        with popup.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(10)])
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
        with popup.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(10)])
            Color(rgba=get_color_from_hex('#FF7043'))
            RoundedRectangle(
                pos=(popup.x + dp(10), popup.y + popup.height - dp(3)),
                size=(popup.width - dp(20), dp(3)),
                radius=[dp(1.5)]
            )
        popup.title_color = get_color_from_hex('#FFFFFF')
        popup.title_size = sp(18)

        logout_btn = Button(
            text='Вийти з акаунту',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            size_hint_y=None,
            height=dp(45),
            font_size=sp(16)
        )
        logout_btn.bind(on_press=lambda x: [popup.dismiss(), self.logout()])

        exit_btn = Button(
            text='Вихід з додатку',
            background_color=get_color_from_hex('#D8F3EB'),
            color=get_color_from_hex('#0A4035'),
            size_hint_y=None,
            height=dp(45),
            font_size=sp(16)
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
            size_hint=(0.85, 0.6),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.7)
        )

        content = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=[dp(20)] * 4,
            opacity=0
        )

        with content.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            self.content_rect = RoundedRectangle(size=content.size, pos=content.pos, radius=[dp(15)])
            Color(rgba=get_color_from_hex('#FFB74D'))
            RoundedRectangle(
                pos=(content.x + dp(15), content.y + content.height - dp(3)),
                size=(content.width - dp(30), dp(3)),
                radius=[dp(1.5)]
            )

        content.bind(size=self._update_rect, pos=self._update_rect)

        # header with icon
        title_box = BoxLayout(size_hint_y=None, height=dp(40), spacing=dp(10))
        icon = BoxLayout(size_hint=(None, None), size=(dp(30), dp(30)))
        with icon.canvas:
            Color(rgba=get_color_from_hex('#FFB74D'))
            Line(points=[icon.center_x - dp(10), icon.center_y + dp(8),
                        icon.center_x + dp(10), icon.center_y + dp(8)], width=dp(2))
            Line(points=[icon.center_x - dp(5), icon.center_y,
                        icon.center_x + dp(5), icon.center_y], width=dp(2))
            Line(points=[icon.center_x, icon.center_y - dp(8),
                        icon.center_x, icon.center_y - dp(8)], width=dp(2))

        title = Label(text='Фільтр транзакцій', font_size=sp(20), bold=True,
                    color=get_color_from_hex('#FFFFFF'), halign='left')
        title_box.add_widget(icon)
        title_box.add_widget(title)

        # styled spinner
        class StyledSpinner(Spinner):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.background_normal = ''
                self.background_down = ''
                self.bold = True
                self.bind(size=self.update_background, pos=self.update_background)

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

        type_spinner = StyledSpinner(
            text='Всі',
            values=['Всі', 'Доходи', 'Витрати'],
            size_hint_y=None,
            height=dp(45),
            color=get_color_from_hex('#0A4035'),
            font_size=sp(16)
        )

        all_categories = ['Всі'] + INCOME_CATEGORIES + EXPENSE_CATEGORIES
        category_spinner = StyledSpinner(
            text='Всі',
            values=all_categories,
            size_hint_y=None,
            height=dp(45),
            color=get_color_from_hex('#0A4035'),
            font_size=sp(16)
        )

        periods = ['Весь час', 'Сьогодні', 'Тиждень', 'Місяць', 'Рік']
        period_spinner = StyledSpinner(
            text='Весь час',
            values=periods,
            size_hint_y=None,
            height=dp(45),
            color=get_color_from_hex('#0A4035'),
            font_size=sp(16)
        )

        # styled input
        class StyledTextInput(TextInput):
            def __init__(self, **kwargs):
                super().__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.cursor_color = get_color_from_hex('#0A4035')
                self.foreground_color = get_color_from_hex('#0A4035')
                self.bold = True
                self.bind(size=self.update_background, pos=self.update_background)

            def update_background(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex('#D8F3EB'))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])

        min_amount = StyledTextInput(hint_text='Від', hint_text_color=get_color_from_hex('#0A4035'),
                                    input_type='number', multiline=False, font_size=sp(16),
                                    padding=[dp(15), dp(12), dp(15), dp(10)])
        max_amount = StyledTextInput(hint_text='До', hint_text_color=get_color_from_hex('#0A4035'),
                                    input_type='number', multiline=False, font_size=sp(16),
                                    padding=[dp(15), dp(12), dp(15), dp(10)])

        amount_box = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(10))
        amount_box.add_widget(min_amount)
        amount_box.add_widget(max_amount)

        # styled button
        class StyledButton(Button):
            def __init__(self, bg_color, **kwargs):
                super().__init__(**kwargs)
                self.background_color = (0, 0, 0, 0)
                self.bg_color = bg_color
                self.color = get_color_from_hex('#FFFFFF')
                self.bind(size=self.update_background, pos=self.update_background)

            def update_background(self, *args):
                self.canvas.before.clear()
                with self.canvas.before:
                    Color(rgba=get_color_from_hex(self.bg_color))
                    RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(8)])

        reset_button = StyledButton(text='Скинути', bg_color='#445555', font_size=sp(16), bold=True)
        apply_button = StyledButton(text='Застосувати', bg_color='#0F7055', font_size=sp(16), bold=True)

        reset_button.bind(on_press=lambda x: self.reset_filter(
            type_spinner, category_spinner, period_spinner, min_amount, max_amount
        ))
        apply_button.bind(on_press=lambda x: self.apply_filter(
            type_spinner.text, category_spinner.text, period_spinner.text,
            min_amount.text, max_amount.text, modal
        ))

        buttons_box = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(15))
        buttons_box.add_widget(reset_button)
        buttons_box.add_widget(apply_button)

        content.add_widget(title_box)

        content.add_widget(Label(
            text='Тип транзакції:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='left',
            size_hint_y=None,
            height=dp(30),
            text_size=(None, dp(30))
        ))
        content.add_widget(type_spinner)

        content.add_widget(Label(
            text='Категорія:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='left',
            size_hint_y=None,
            height=dp(30),
            text_size=(None, dp(30))
        ))
        content.add_widget(category_spinner)

        content.add_widget(Label(
            text='Період:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='left',
            size_hint_y=None,
            height=dp(30),
            text_size=(None, dp(30))
        ))
        content.add_widget(period_spinner)

        content.add_widget(Label(
            text='Сума:',
            font_size=sp(16),
            color=get_color_from_hex('#FFFFFF'),
            halign='left',
            size_hint_y=None,
            height=dp(30),
            text_size=(None, dp(30))
        ))
        content.add_widget(amount_box)

        content.add_widget(Widget())  # expanding space filler
        content.add_widget(buttons_box)


        modal.add_widget(content)
        modal.open()
        Animation(opacity=1, d=0.3).start(content)

    def reset_filter(self, type_spinner, category_spinner, period_spinner, min_amount, max_amount):
        type_spinner.text = 'Всі'
        category_spinner.text = 'Всі'
        period_spinner.text = 'Весь час'
        min_amount.text = ''
        max_amount.text = ''

    def apply_filter(self, type_filter, category_filter, period_filter, min_amount_text, max_amount_text, modal):
        try:
            modal.dismiss()
            min_amount = float(min_amount_text.replace(',', '.')) if min_amount_text else None
            max_amount = float(max_amount_text.replace(',', '.')) if max_amount_text else None

            self.transactions_container.clear_widgets()
            now = datetime.now()

            if period_filter == 'Сьогодні':
                date_from = now.replace(hour=0, minute=0, second=0, microsecond=0)
            elif period_filter == 'Тиждень':
                date_from = now - timedelta(days=7)
            elif period_filter == 'Місяць':
                date_from = now - timedelta(days=30)
            elif period_filter == 'Рік':
                date_from = now - timedelta(days=365)
            else:
                date_from = now - timedelta(days=3650)

            for _ in range(15):
                if type_filter == 'Доходи':
                    is_income = True
                elif type_filter == 'Витрати':
                    is_income = False
                else:
                    is_income = random.choice([True, False])

                category = category_filter if category_filter != 'Всі' else random.choice(
                    INCOME_CATEGORIES if is_income else EXPENSE_CATEGORIES)

                amount = random.randint(100, 10000) if is_income else -random.randint(100, 5000)

                if min_amount is not None and amount < min_amount:
                    continue
                if max_amount is not None and amount > max_amount:
                    continue

                transaction_date = now - timedelta(days=random.randint(0, 100))
                if transaction_date < date_from:
                    continue

                date_str = transaction_date.strftime("%d.%m.%Y")

                transaction_row = Builder.load_string(f'''
TransactionRow:
    category: '{category}'
    amount: '{amount:+,.0f}'
    date: '{date_str}'
    is_income: {is_income}
''')
                self.transactions_container.add_widget(transaction_row)

            self.show_success_message("Фільтр застосовано")

        except ValueError:
            self.show_error_message("Некоректне значення суми")
        except Exception as e:
            self.show_error_message(f"Помилка фільтрації: {str(e)}")

    def show_success_message(self, message):
        popup = Popup(
            title='Успіх',
            content=Label(text=message),
            size_hint=(0.7, 0.3),
            background='',
            background_color=(0, 0, 0, 0)
        )
        with popup.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            RoundedRectangle(pos=popup.pos, size=popup.size, radius=[dp(10)])
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
        Clock.schedule_once(lambda dt: popup.dismiss(), 2)

    def exit_app(self):
        from kivy.core.window import Window
        Window.close()