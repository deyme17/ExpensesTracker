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

from app.views.screens.base_screen import BaseScreen
from app.views.widgets.transaction_row import TransactionRow
from app.views.widgets.custom_buttons import RoundedButton, FloatingActionButton, SegmentedButton
from app.views.widgets.custom_inputs import (
    StyledTextInput, CustomSpinner, SpinnerOption, DateInput, 
    LabeledInput, LabeledSpinner, LabeledDateInput
)
from app.views.widgets.custom_popups import ConfirmationPopup, ErrorPopup, SuccessPopup
from app.utils.constants import (
    PAYMENT_METHOD_ALL, PAYMENT_METHOD_CARD, PAYMENT_METHOD_CASH,
    TRANSACTION_TYPE_ALL, TRANSACTION_TYPE_INCOME, TRANSACTION_TYPE_EXPENSE,
    INCOME_CATEGORIES, EXPENSE_CATEGORIES, CURRENCY_UAH, CURRENCY_EUR, CURRENCY_USD
)
from app.utils.formatters import format_amount, format_date
from app.utils.theme import (
    get_primary_color, get_secondary_color, get_accent_color, 
    get_text_primary_color, get_income_color, get_expense_color,
    PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR
)

# Load kv file
Builder.load_file('kv/transactions_screen.kv')


class TransactionsScreen(BaseScreen):
    """
    Transactions screen for displaying and managing transactions.
    
    This screen shows a list of transactions and provides functionality for
    adding, editing, filtering, and sorting transactions.
    """
    controller = ObjectProperty(None)
    
    def __init__(self, **kwargs):
        super(TransactionsScreen, self).__init__(**kwargs)
        self.transactions_data = {}

    def show_add_transaction(self, is_income=True):
        """Show dialog for adding a new transaction."""
        # modal view
        modal = ModalView(
            size_hint=(0.85, 0.9),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.7)
        )
        
        # content
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=[dp(20), dp(20), dp(20), dp(20)],
            opacity=0
        )
        
        with content.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            content_rect = RoundedRectangle(size=content.size, pos=content.pos, radius=[dp(15)])
            
        content.bind(size=lambda instance, value: setattr(content_rect, 'size', instance.size))
        content.bind(pos=lambda instance, value: setattr(content_rect, 'pos', instance.pos))

        
        # title
        title_text = 'Додати дохід' if is_income else 'Додати витрату'
        title_label = Label(
            text=title_text,
            font_size=sp(20),
            bold=True,
            color=get_text_primary_color(),
            halign='center',
            size_hint_y=None,
            height=dp(40)
        )
        
        # fields in a scroll view
        scroll_view = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            size_hint=(1, 1)
        )
        
        # fields container
        fields_container = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None
        )
        fields_container.bind(minimum_height=fields_container.setter('height'))
        
        # category
        categories = INCOME_CATEGORIES if is_income else EXPENSE_CATEGORIES
        category_input = LabeledSpinner(
            label_text='Категорія:',
            values=categories,
            selected=categories[0] if categories else ""
        )
        
        # payment method
        payment_input = LabeledSpinner(
            label_text='Тип оплати:',
            values=[PAYMENT_METHOD_CARD, PAYMENT_METHOD_CASH],
            selected=PAYMENT_METHOD_CARD
        )
        
        # amount
        amount_input = LabeledInput(
            label_text='Сума:',
            hint_text='Введіть суму'
        )
        
        # currency
        currency_input = LabeledSpinner(
            label_text='Валюта:',
            values=[CURRENCY_UAH, CURRENCY_EUR, CURRENCY_USD],
            selected=CURRENCY_UAH
        )
        
        # date
        date_input = LabeledDateInput(
            label_text='Дата:'
        )
        
        # cashback
        cashback_input = LabeledInput(
            label_text='Кешбек:',
            hint_text='Введіть відсоток кешбеку',
            text='0'
        )
        
        # commission
        commission_input = LabeledInput(
            label_text='Комісія:',
            hint_text='Введіть комісію',
            text='0'
        )
        
        # description
        description_input = LabeledInput(
            label_text='Опис:',
            hint_text='Додайте опис транзакції'
        )
        
        # add fields to container
        fields_container.add_widget(category_input)
        fields_container.add_widget(payment_input)
        fields_container.add_widget(amount_input)
        fields_container.add_widget(currency_input)
        fields_container.add_widget(date_input)
        fields_container.add_widget(cashback_input)
        fields_container.add_widget(commission_input)
        fields_container.add_widget(description_input)
        
        # add fields container to scroll view
        scroll_view.add_widget(fields_container)
        
        # buttons
        buttons_box = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(15)
        )
        
        cancel_button = RoundedButton(
            text='Скасувати',
            bg_color='#445555',
            size_hint_y=None,
            height=dp(50),
            font_size=sp(16)
        )
        
        save_button = RoundedButton(
            text='Зберегти',
            bg_color='#0F7055',
            size_hint_y=None,
            height=dp(50),
            font_size=sp(16)
        )
        
        buttons_box.add_widget(cancel_button)
        buttons_box.add_widget(save_button)
        
        # add all elements to content
        content.add_widget(title_label)
        content.add_widget(scroll_view)
        content.add_widget(buttons_box)
        
        modal.add_widget(content)
        
        # bind button
        cancel_button.bind(on_press=lambda x: modal.dismiss())
        save_button.bind(on_press=lambda x: self._save_transaction(
            is_income,
            category_input.selected,
            amount_input.text,
            date_input.date_text,
            description_input.text,
            payment_input.selected,
            currency_input.selected,
            cashback_input.text,
            commission_input.text,
            modal
        ))
        
        modal.open()
        Animation(opacity=1, d=0.3).start(content)
    
    def _save_transaction(self, is_income, category, amount, date, description, 
                         payment_method, currency='UAH', cashback='0', commission='0', modal=None):
        """Save a new transaction."""
        if not self.controller:
            return
        
        # add transaction via controller
        transaction, message = self.controller.add_transaction(
            category=category,
            amount=amount,
            date=date,
            description=description,
            is_income=is_income,
            payment_method=payment_method,
            currency=currency,
            cashback=cashback,
            commission=commission
        )
        
        if transaction:
            if modal:
                modal.dismiss()
            
            self.show_success_message(message)
            
            Clock.schedule_once(self._load_transactions, 0.2)
        else:
            self.show_error_message(message)
    
    def show_transaction_details(self, transaction_id):
        """Show transaction details in a modal view."""
        if not self.controller:
            return

        transaction = self.controller.show_transaction_details(transaction_id)
        if not transaction:
            self.show_error_message("Транзакцію не знайдено")
            return

        # modal view
        modal = ModalView(
            size_hint=(0.85, 0.75),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.6)
        )
        
        # content
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
        
        # title
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
        
        # scroll view for details
        scroll_view = ScrollView(do_scroll_x=False)
        details_layout = GridLayout(
            cols=1,
            spacing=dp(10),
            size_hint_y=None,
            padding=[dp(10), dp(5)]
        )
        details_layout.bind(minimum_height=details_layout.setter('height'))
        
        # helper function to add detail rows
        def add_detail_row(label_text, value_text):
            row = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(30),
                spacing=dp(10)
            )
            
            label = Label(
                text=f"{label_text}:",
                font_size=sp(16),
                color=get_color_from_hex('#FFFFFF'),
                halign='left',
                size_hint_x=0.4,
                text_size=(None, None)
            )
            
            value = Label(
                text=str(value_text),
                font_size=sp(16),
                color=get_color_from_hex('#D8F3EB'),
                halign='left',
                size_hint_x=0.6,
                text_size=(None, None)
            )
            
            row.add_widget(label)
            row.add_widget(value)
            return row
        
        # add details to layout
        details_layout.add_widget(add_detail_row("Категорія", transaction.category))
        
        # add amount with currency
        try:
            amount_value = abs(float(transaction.amount))
            amount_text = f"{'+' if transaction.is_income else '-'}{amount_value:,.2f} ({transaction.currency})"
        except ValueError:
            amount_text = f"{transaction.amount} ({transaction.currency})"
        
        details_layout.add_widget(add_detail_row("Сума", amount_text))
        
        # format date
        formatted_date = transaction.get_formatted_date()
        
        details_layout.add_widget(add_detail_row("Дата", formatted_date))
        details_layout.add_widget(add_detail_row("Тип оплати", transaction.payment_method))
        
        # cashback and commission
        try:
            cashback_value = float(transaction.cashback)
            if cashback_value > 0:
                details_layout.add_widget(add_detail_row("Кешбек", f"{cashback_value}"))
        except (ValueError, TypeError):
            pass
        
        try:
            commission_value = float(transaction.commission)
            if commission_value > 0:
                details_layout.add_widget(add_detail_row("Комісія", f"{commission_value}"))
        except (ValueError, TypeError):
            pass
        
        # description
        if transaction.description and transaction.description.strip():
            description_layout = BoxLayout(
                orientation='horizontal',
                size_hint_y=None,
                height=dp(100),
                spacing=dp(10),
                padding=[dp(10), 0, dp(10), 0]
            )
            
            desc_label = Label(
                text="Опис:",
                font_size=sp(16),
                color=get_color_from_hex('#FFFFFF'),
                size_hint_x=0.3,
                halign='left',
                valign='top',
                text_size=(None, None)
            )
            
            desc_text_label = Label(
                text=transaction.description,
                font_size=sp(16),
                color=get_color_from_hex('#D8F3EB'),
                halign='left',
                valign='top',
                text_size=(0, None)
            )
            
            def update_text_size(instance, value):
                instance.text_size = (instance.width, None)
            
            desc_text_label.bind(size=update_text_size)

            description_layout.add_widget(desc_label)
            description_layout.add_widget(desc_text_label)
            details_layout.add_widget(description_layout)

        
        # details layout to scroll view
        scroll_view.add_widget(details_layout)
        
        buttons_layout = BoxLayout(
            orientation='horizontal',
            size_hint_y=None,
            height=dp(50),
            spacing=dp(10)
        )
        
        edit_button = RoundedButton(
            text="[b]Редагувати[/b]",
            bg_color="#0F7055",
            size_hint_x=0.33,
            font_size=dp(14),
            markup=True
        )

        edit_button.bind(on_press=lambda x: [
            modal.dismiss(),
            self.show_edit_transaction(transaction.transaction_id)
        ])
        
        delete_button = RoundedButton(
            text="[b]Видалити[/b]",
            bg_color="#F44336",
            size_hint_x=0.33,
            font_size=dp(14),
            markup=True
        )
        delete_button.bind(on_press=lambda x: [
            modal.dismiss(),
            self.confirm_delete_transaction([transaction.transaction_id])
        ])
        
        close_button = RoundedButton(
            text="[b]Закрити[/b]",
            bg_color="#445555",
            size_hint_x=0.33,
            font_size=dp(14),
            markup=True
        )
        close_button.bind(on_press=lambda x: modal.dismiss())
        
        # buttons
        buttons_layout.add_widget(edit_button)
        buttons_layout.add_widget(delete_button)
        buttons_layout.add_widget(close_button)
        
        # add widgets to content
        content.add_widget(title)
        content.add_widget(scroll_view)
        content.add_widget(buttons_layout)
        
        # add content to modal
        modal.add_widget(content)
        
        modal.open()
        Animation(opacity=1, d=0.3).start(content)

    def add_refresh_button(self):
        """Add refresh button to the UI."""
        refresh_button = FloatingActionButton(
            size_hint=(None, None),
            size=(dp(56), dp(56)),
            pos_hint={'right': 0.95, 'top': 0.95},
            bg_color=get_accent_color()
        )

        refresh_button.bind(on_press=self.refresh_transactions)

        self.add_widget(refresh_button)

    def add_refresh_button(self):
        """Add refresh button to the UI."""
        refresh_button = FloatingActionButton(
            size_hint=(None, None),
            size=(dp(56), dp(56)),
            pos_hint={'right': 0.95, 'top': 0.95},
            bg_color=get_accent_color()
        )

        refresh_button.bind(on_press=self.refresh_transactions)

        self.add_widget(refresh_button)

    def refresh_transactions(self, instance=None):
        """Refresh transactions list."""
        if not self.controller:
            return
        
        def do_refresh(dt):
            transactions = self.controller.get_transactions(force_refresh=True)
            
            # update ui
            self.transactions_container.clear_widgets()
            self.transactions_data = {}
            
            for transaction in transactions:
                row = TransactionRow(
                    transaction_id=transaction.transaction_id,
                    category=transaction.category,
                    amount=str(abs(transaction.amount)),
                    date=transaction.get_formatted_date(),
                    is_income=transaction.is_income,
                    payment_method=transaction.payment_method,
                    description=transaction.description,
                    currency=transaction.currency,
                    cashback=str(transaction.cashback),
                    commission=str(transaction.commission),
                    controller=self.controller,
                    transactions_screen=self
                )
                self.transactions_container.add_widget(row)
                self.transactions_data[transaction.transaction_id] = transaction
        
        Clock.schedule_once(do_refresh, 0.2)
        
    def show_edit_transaction(self, transaction_id):
        """Show dialog for editing a transaction."""
        if not self.controller or transaction_id not in self.transactions_data:
            return
        
        transaction = self.transactions_data[transaction_id]
        
        # modal view
        modal = ModalView(
            size_hint=(0.9, 0.9),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.7)
        )
        
        # content
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(15),
            padding=[dp(20), dp(20), dp(20), dp(20)],
            opacity=0
        )
        
        with content.canvas.before:
            Color(rgba=get_primary_color())
            self.content_rect = RoundedRectangle(size=content.size, pos=content.pos, radius=[dp(15)])
        
        content.bind(size=self._update_rect, pos=self._update_rect)
        
        # title
        title_label = Label(
            text='Редагувати транзакцію',
            font_size=sp(20),
            bold=True,
            color=get_text_primary_color(),
            halign='center',
            size_hint_y=None,
            height=dp(40)
        )
        
        # add fields in a scroll view
        scroll_view = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            size_hint=(1, 1)
        )
        
        # fields container
        fields_container = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            size_hint_y=None
        )
        fields_container.bind(minimum_height=fields_container.setter('height'))
        
        # category
        categories = INCOME_CATEGORIES if transaction.is_income else EXPENSE_CATEGORIES
        category_input = LabeledSpinner(
            label_text='Категорія:',
            values=categories,
            selected=transaction.category
        )
        
        # payment method
        payment_input = LabeledSpinner(
            label_text='Тип оплати:',
            values=[PAYMENT_METHOD_CARD, PAYMENT_METHOD_CASH],
            selected=transaction.payment_method
        )
        
        # amount
        amount_input = LabeledInput(
            label_text='Сума:',
            hint_text='Введіть суму',
            text=str(abs(transaction.amount))
        )
        
        # currency
        currency_input = LabeledSpinner(
            label_text='Валюта:',
            values=[CURRENCY_UAH, CURRENCY_EUR, CURRENCY_USD],
            selected=transaction.currency
        )
        
        # date
        date_input = LabeledDateInput(
            label_text='Дата:'
        )

        date_input.date_text = transaction.get_formatted_date()
        
        # cashback
        cashback_input = LabeledInput(
            label_text='Кешбек:',
            hint_text='Введіть відсоток кешбеку',
            text=str(transaction.cashback)
        )
        
        # commission
        commission_input = LabeledInput(
            label_text='Комісія:',
            hint_text='Введіть комісію',
            text=str(transaction.commission)
        )
        
        # description
        description_input = LabeledInput(
            label_text='Опис:',
            hint_text='Додайте опис транзакції',
            text=transaction.description
        )
        
        # add fields to container
        fields_container.add_widget(category_input)
        fields_container.add_widget(payment_input)
        fields_container.add_widget(amount_input)
        fields_container.add_widget(currency_input)
        fields_container.add_widget(date_input)
        fields_container.add_widget(cashback_input)
        fields_container.add_widget(commission_input)
        fields_container.add_widget(description_input)
        
        # add fields container to scroll view
        scroll_view.add_widget(fields_container)
        
        # buttons
        buttons_box = BoxLayout(
            size_hint_y=None,
            height=dp(50),
            spacing=dp(15)
        )
        
        cancel_button = RoundedButton(
            text='Скасувати',
            bg_color='#445555',
            size_hint_y=None,
            height=dp(50),
            font_size=sp(16)
        )
        
        save_button = RoundedButton(
            text='Зберегти',
            bg_color='#0F7055',
            size_hint_y=None,
            height=dp(50),
            font_size=sp(16)
        )
        
        buttons_box.add_widget(cancel_button)
        buttons_box.add_widget(save_button)
        
        # add all elements to content
        content.add_widget(title_label)
        content.add_widget(scroll_view)
        content.add_widget(buttons_box)
        
        modal.add_widget(content)
        
        # bind button
        cancel_button.bind(on_press=lambda x: modal.dismiss())
        save_button.bind(on_press=lambda x: self._update_transaction(
            transaction_id,
            category_input.selected,
            amount_input.text,
            date_input.date_text,
            description_input.text,
            transaction.is_income,
            payment_input.selected,
            currency_input.selected,
            cashback_input.text,
            commission_input.text,
            modal
        ))
        
        modal.open()
        Animation(opacity=1, d=0.3).start(content)
    
    def _update_transaction(self, transaction_id, category, amount, date, description, 
                           is_income, payment_method, currency='UAH', cashback='0', 
                           commission='0', modal=None):
        """Update an existing transaction."""
        if not self.controller:
            return
        
        # update transaction via controller
        transaction, message = self.controller.update_transaction(
            transaction_id=transaction_id,
            category=category,
            amount=amount,
            date=date,
            description=description,
            is_income=is_income,
            payment_method=payment_method,
            currency=currency,
            cashback=cashback,
            commission=commission
        )
        
        if transaction:
            if modal:
                modal.dismiss()
            
            self.show_success_message(message)
            
            Clock.schedule_once(self._load_transactions, 0.2)
        else:
            self.show_error_message(message)
    
    def confirm_delete_transaction(self, transaction_id):
        """Show confirmation dialog for deleting a transaction."""
        if not transaction_id:
            return
        
        confirmation = ConfirmationPopup(
            message="Ви впевнені, що хочете видалити цю транзакцію?",
            on_confirm=lambda: self._delete_transaction(transaction_id)
        )
        
        confirmation.open()

    def _delete_transaction(self, transaction_id):
        """Delete a transaction."""
        if not self.controller:
            return

        if isinstance(transaction_id, list):
            transaction_id = transaction_id[0]
        
        # delete transaction via controller
        success, message = self.controller.delete_transaction(transaction_id)
        
        if success:
            self.show_success_message(message)
            
            if transaction_id in self.transactions_data:
                del self.transactions_data[transaction_id]

            Clock.schedule_once(self._load_transactions, 0.2)
        else:
            self.show_error_message(message)
    
    def show_filter(self):
        """Show dialog for filtering transactions."""
        # modal
        modal = ModalView(
            size_hint=(0.85, 0.9),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.7)
        )

        content_scroll = ScrollView(
            do_scroll_x=False,
            do_scroll_y=True,
            size_hint=(1, 1)
        )
        
        # content
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(12),
            padding=[dp(20), dp(20), dp(20), dp(20)],
            opacity=0,
            size_hint_y=None
        )
        content.bind(minimum_height=content.setter('height'))
        
        with content.canvas.before:
            Color(rgba=get_primary_color())
            self.content_rect = RoundedRectangle(size=content.size, pos=content.pos, radius=[dp(20)])
        
        content.bind(size=self._update_rect, pos=self._update_rect)
        
        # title
        title_label = Label(
            text='Фільтр транзакцій',
            font_size=sp(22),
            bold=True,
            color=get_text_primary_color(),
            halign='center',
            size_hint_y=None,
            height=dp(50)
        )
        
        # amount range
        amount_label = Label(
            text='Сума:',
            font_size=sp(16),
            color=get_text_primary_color(),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        amount_row = BoxLayout(
            size_hint_y=None,
            height=dp(45),
            spacing=dp(10)
        )
        
        min_amount_box = BoxLayout(
            size_hint_x=0.5,
            spacing=dp(5)
        )
        
        min_amount_label = Label(
            text="З:",
            size_hint=(None, 1),
            width=dp(20),
            color=get_text_primary_color(),
            font_size=sp(16)
        )
        
        min_amount = StyledTextInput(
            hint_text='0',
            text='0',
            hint_text_color=get_color_from_hex('#0A4035')
        )
        
        min_amount_box.add_widget(min_amount_label)
        min_amount_box.add_widget(min_amount)
        
        max_amount_box = BoxLayout(
            size_hint_x=0.5,
            spacing=dp(5)
        )
        
        max_amount_label = Label(
            text="До:",
            size_hint=(None, 1),
            width=dp(25),
            color=get_text_primary_color(),
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
        
        # date range
        date_section = BoxLayout(
            orientation='vertical',
            spacing=dp(8),
            size_hint_y=None,
            height=dp(180),
            padding=[dp(10), dp(10), dp(10), dp(10)]
        )
        
        with date_section.canvas.before:
            Color(rgba=(0.09, 0.50, 0.45, 1))
            date_rect = RoundedRectangle(pos=date_section.pos, size=date_section.size, radius=[dp(12)])

        def update_date_rect(instance, value):
            date_rect.pos = instance.pos
            date_rect.size = instance.size
        
        date_section.bind(pos=update_date_rect, size=update_date_rect)
        
        date_title = Label(
            text="Інтервал дат:",
            font_size=sp(16),
            color=get_text_primary_color(),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        date_section.add_widget(date_title)
        
        # start date label
        start_date_label = Label(
            text="З:",
            font_size=sp(16),
            color=get_text_primary_color(),
            halign='left',
            size_hint_y=None,
            height=dp(25)
        )
        date_section.add_widget(start_date_label)
        
        # days, months, years for spinners
        from datetime import datetime
        days = [str(i).zfill(2) for i in range(1, 32)]
        months = [str(i).zfill(2) for i in range(1, 13)]
        current_year = datetime.now().year
        years = [str(year) for year in range(current_year - 5, current_year + 1)]
        
        # start date row
        start_date_row = BoxLayout(
            orientation='horizontal',
            spacing=dp(5),
            size_hint_y=None,
            height=dp(45)
        )
        
        start_day_spinner = CustomSpinner(
            text='01',
            values=days,
            size_hint=(0.3, 1),
            padding_x=dp(25)
        )
        
        start_month_spinner = CustomSpinner(
            text='01',
            values=months,
            size_hint=(0.3, 1),
            padding_x=dp(25)
        )
        
        start_year_spinner = CustomSpinner(
            text=str(current_year - 1),
            values=years,
            size_hint=(0.4, 1),
            padding_x=dp(25)
        )
        
        start_date_row.add_widget(start_day_spinner)
        start_date_row.add_widget(start_month_spinner)
        start_date_row.add_widget(start_year_spinner)
        
        date_section.add_widget(start_date_row)
        
        # end date label
        end_date_label = Label(
            text="До:",
            font_size=sp(16),
            color=get_text_primary_color(),
            halign='left',
            size_hint_y=None,
            height=dp(25)
        )
        date_section.add_widget(end_date_label)
        
        # end date row
        end_date_row = BoxLayout(
            orientation='horizontal',
            spacing=dp(5),
            size_hint_y=None,
            height=dp(45)
        )
        
        end_day_spinner = CustomSpinner(
            text=str(datetime.now().day).zfill(2),
            values=days,
            size_hint=(0.3, 1),
            padding_x=dp(25)
        )
        
        end_month_spinner = CustomSpinner(
            text=str(datetime.now().month).zfill(2),
            values=months,
            size_hint=(0.3, 1),
            padding_x=dp(25)
        )
        
        end_year_spinner = CustomSpinner(
            text=str(current_year),
            values=years,
            size_hint=(0.4, 1),
            padding_x=dp(25)
        )
        
        end_date_row.add_widget(end_day_spinner)
        end_date_row.add_widget(end_month_spinner)
        end_date_row.add_widget(end_year_spinner)
        
        date_section.add_widget(end_date_row)
        
        # transaction type
        type_label = Label(
            text='Тип транзакції:',
            font_size=sp(16),
            color=get_text_primary_color(),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        type_spinner = CustomSpinner(
            text='Всі',
            values=['Всі', 'Доходи', 'Витрати'],
            size_hint_y=None,
            height=dp(45),
            padding_x=dp(25)
        )
        
        # payment method
        payment_label = Label(
            text='Спосіб оплати:',
            font_size=sp(16),
            color=get_text_primary_color(),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        payment_method_spinner = CustomSpinner(
            text='Всі',
            values=['Всі', 'Картка', 'Готівка'],
            size_hint_y=None,
            height=dp(45),
            padding_x=dp(25)
        )
        
        # buttons
        buttons_box = BoxLayout(
            size_hint_y=None,
            height=dp(45),
            spacing=dp(15)
        )
        
        reset_button = RoundedButton(
            text='Скинути',
            bg_color='#445555'
        )
        
        apply_button = RoundedButton(
            text='Застосувати',
            bg_color='#0F7055'
        )
        
        # bind button actions
        reset_button.bind(on_press=lambda x: self._reset_filter(
            type_spinner=type_spinner, 
            min_amount=min_amount, 
            max_amount=max_amount,
            start_day_spinner=start_day_spinner, 
            start_month_spinner=start_month_spinner, 
            start_year_spinner=start_year_spinner,
            end_day_spinner=end_day_spinner, 
            end_month_spinner=end_month_spinner, 
            end_year_spinner=end_year_spinner,
            payment_method_spinner=payment_method_spinner
        ))
        
        apply_button.bind(on_press=lambda x: self._apply_filter(
            type_spinner.text,
            min_amount.text, 
            max_amount.text,
            f"{start_day_spinner.text}.{start_month_spinner.text}.{start_year_spinner.text}",
            f"{end_day_spinner.text}.{end_month_spinner.text}.{end_year_spinner.text}",
            payment_method_spinner.text,
            modal
        ))
        
        buttons_box.add_widget(reset_button)
        buttons_box.add_widget(apply_button)
        
        # add all elements to content
        content.add_widget(title_label)
        content.add_widget(amount_label)
        content.add_widget(amount_row)
        content.add_widget(Widget())  # space1
        content.add_widget(Widget())  # space2
        content.add_widget(date_section)
        content.add_widget(type_label)
        content.add_widget(type_spinner)
        content.add_widget(payment_label)
        content.add_widget(payment_method_spinner)
        content.add_widget(Widget())  # space
        content.add_widget(buttons_box)
        
        # add content to modal
        content_scroll.add_widget(content)
        modal.add_widget(content_scroll)
        
        modal.open()
        Animation(opacity=1, d=0.3).start(content)
    
    def _reset_filter(self, type_spinner, category_spinner=None, min_amount=None, max_amount=None,
                    start_day_spinner=None, start_month_spinner=None, start_year_spinner=None,
                    end_day_spinner=None, end_month_spinner=None, end_year_spinner=None,
                    payment_method_spinner=None):
        """Reset filter inputs to default values."""
        if type_spinner:
            type_spinner.text = 'Всі'
        if category_spinner:
            category_spinner.text = 'Всі'
        if payment_method_spinner:
            payment_method_spinner.text = 'Всі'
        if min_amount:
            min_amount.text = '0'
        if max_amount:
            max_amount.text = '1000000'

        from datetime import datetime
        current_year = datetime.now().year
        
        if start_day_spinner:
            start_day_spinner.text = '01'
        if start_month_spinner:
            start_month_spinner.text = '01'
        if start_year_spinner:
            start_year_spinner.text = str(current_year - 1)

        if end_day_spinner:
            end_day_spinner.text = str(datetime.now().day).zfill(2)
        if end_month_spinner:
            end_month_spinner.text = str(datetime.now().month).zfill(2)
        if end_year_spinner:
            end_year_spinner.text = str(current_year)
    
    def _apply_filter(self, type_filter, min_amount_text, max_amount_text,
                    start_date, end_date, payment_method, modal):
        """Apply the selected filter."""
        if not self.controller:
            return
        
        try:
            # parse amount range
            min_amount = float(min_amount_text.replace(',', '.')) if min_amount_text else 0
            max_amount = float(max_amount_text.replace(',', '.')) if max_amount_text else float('inf')
            
            # parse dates
            from app.utils.validators import validate_date
            
            start_date_valid, start_date_obj = validate_date(start_date)
            if not start_date_valid:
                start_date_obj = datetime.now() - timedelta(days=365)
            
            end_date_valid, end_date_obj = validate_date(end_date)
            if not end_date_valid:
                end_date_obj = datetime.now()
            
            # convert transaction type
            transaction_type = None
            if type_filter == TRANSACTION_TYPE_INCOME:
                transaction_type = True
            elif type_filter == TRANSACTION_TYPE_EXPENSE:
                transaction_type = False
            
            # convert payment method
            if payment_method == PAYMENT_METHOD_ALL:
                payment_method = None
            
            # apply filter via controller
            filtered_transactions = self.controller.filter_transactions(
                min_amount=min_amount,
                max_amount=max_amount,
                start_date=start_date_obj,
                end_date=end_date_obj,
                transaction_type=transaction_type,
                payment_method=payment_method
            )
            
            # clear existing transactions
            self.transactions_container.clear_widgets()
            self.transactions_data = {}
            
            # add filtered transactions
            for transaction in filtered_transactions:
                row = TransactionRow(
                    transaction_id=transaction.transaction_id,
                    category=transaction.category,
                    amount=str(abs(transaction.amount)),
                    date=transaction.get_formatted_date(),
                    is_income=transaction.is_income,
                    payment_method=transaction.payment_method,
                    description=transaction.description,
                    currency=transaction.currency,
                    cashback=str(transaction.cashback),
                    commission=str(transaction.commission),
                    controller=self.controller,
                    transactions_screen=self
                )
                self.transactions_container.add_widget(row)
                
                # store transactions
                self.transactions_data[transaction.transaction_id] = transaction
            
            if modal:
                modal.dismiss()
            
            self.show_success_message("Фільтр застосовано")
            
        except ValueError:
            self.show_error_message("Некоректне значення суми")
        except Exception as e:
            self.show_error_message(f"Помилка фільтрації: {str(e)}")
    
    def show_sort(self):
        """Show dialog for sorting transactions."""
        # modal
        modal = ModalView(
            size_hint=(0.8, 0.6),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.7)
        )
        
        # content
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(12),
            padding=[dp(20), dp(20), dp(20), dp(20)],
            opacity=0
        )
        
        with content.canvas.before:
            Color(rgba=get_primary_color())
            self.content_rect = RoundedRectangle(size=content.size, pos=content.pos, radius=[dp(20)])
        
        content.bind(size=self._update_rect, pos=self._update_rect)
        
        # title
        title_label = Label(
            text='Сортування транзакцій',
            font_size=sp(22),
            bold=True,
            color=get_text_primary_color(),
            halign='center',
            size_hint_y=None,
            height=dp(50)
        )
        
        sort_fields = ['Дата', 'Сума', 'Кешбек', 'Комісія']
        
        field_label = Label(
            text='Сортувати за:',
            font_size=sp(16),
            color=get_text_primary_color(),
            halign='center',
            size_hint_y=None,
            height=dp(30)
        )
        
        field_spinner = CustomSpinner(
            text=sort_fields[0],
            values=sort_fields,
            size_hint_y=None,
            height=dp(45)
        )
        
        # sort direction
        direction_label = Label(
            text='Напрямок:',
            font_size=sp(16),
            color=get_text_primary_color(),
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
        
        # buttons
        buttons_box = BoxLayout(
            size_hint_y=None,
            height=dp(45),
            spacing=dp(15)
        )
        
        cancel_button = RoundedButton(
            text='Скасувати',
            bg_color='#445555'
        )
        
        apply_button = RoundedButton(
            text='Застосувати',
            bg_color='#0F7055'
        )
        
        # bind button actions
        cancel_button.bind(on_press=lambda x: modal.dismiss())
        apply_button.bind(on_press=lambda x: self._apply_sort(
            field_spinner.text,
            direction_spinner.text == 'За зростанням',
            modal
        ))
        
        buttons_box.add_widget(cancel_button)
        buttons_box.add_widget(apply_button)
        
        # add all elements to content
        content.add_widget(title_label)
        content.add_widget(field_label)
        content.add_widget(field_spinner)
        content.add_widget(direction_label)
        content.add_widget(direction_spinner)
        content.add_widget(Widget())  # Spacer
        content.add_widget(buttons_box)
        
        # add content to modal
        modal.add_widget(content)
        
        modal.open()
        Animation(opacity=1, d=0.3).start(content)
    
    def _apply_sort(self, field, ascending, modal):
        """Apply the selected sort order."""
        if not self.controller:
            return
   
        if modal:
            modal.dismiss()
        
        transactions = list(self.transactions_container.children)
        
        def sort_key(transaction):
            if field == 'Дата':
                day, month, year = map(int, transaction.date.split('.'))
                from datetime import datetime
                return datetime(year, month, day)
            
            elif field == 'Сума':
                amount_str = transaction.amount.replace('+', '').replace('-', '').replace(' ', '').replace(',', '.')
                return float(amount_str)
            
            elif field == 'Кешбек':
                try:
                    return float(transaction.cashback.replace(',', '.'))
                except ValueError:
                    return 0
                
            elif field == 'Комісія':
                try:
                    return float(transaction.commission.replace(',', '.'))
                except ValueError:
                    return 0
                
            return 0 
        
        # sort
        try:
            sorted_transactions = sorted(transactions, key=sort_key, reverse=not ascending)
            
            # update ui
            self.transactions_container.clear_widgets()
            for transaction in sorted_transactions:
                self.transactions_container.add_widget(transaction)

            sort_direction = "за зростанням" if ascending else "за спаданням"
            self.show_success_message(f"Транзакції відсортовано за {field.lower()} {sort_direction}")

        except Exception as e:
            self.show_error_message(f"Помилка сортування: {str(e)}")

    def _load_transactions(self, dt=None):
        """Load transactions from the controller."""
        if not self.controller:
            return
        
        self.transactions_container.clear_widgets()
        self.transactions_data = {}
     
        transactions = self.controller.get_transactions()
        
        # add transactions to the ui
        for transaction in transactions:
            row = TransactionRow(
                transaction_id=transaction.transaction_id,
                category=transaction.category,
                amount=str(abs(transaction.amount)),
                date=transaction.get_formatted_date(),
                is_income=transaction.is_income,
                payment_method=transaction.payment_method,
                description=transaction.description,
                currency=transaction.currency,
                cashback=str(transaction.cashback),
                commission=str(transaction.commission),
                controller=self.controller,
                transactions_screen=self
            )
            self.transactions_container.add_widget(row)
            
            # store transactions
            self.transactions_data[transaction.transaction_id] = transaction
    
    def go_analytics(self):
        """Navigate to the analytics screen."""
        self.switch_screen('analytics', 'left')
    
    def show_menu(self):
        """Show application menu."""
        # modal
        popup = ModalView(
            size_hint=(0.7, 0.25),
            background='',
            background_color=(0, 0, 0, 0),
            overlay_color=(0, 0, 0, 0.7)
        )
        
        # content
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(10),
            padding=dp(10)
        )
        
        with content.canvas.before:
            Color(rgba=get_primary_color())
            self.content_rect = RoundedRectangle(size=content.size, pos=content.pos, radius=[dp(10)])
        
        content.bind(size=self._update_rect, pos=self._update_rect)
        
        # title
        title_label = Label(
            text='Меню',
            font_size=sp(18),
            bold=True,
            color=get_text_primary_color(),
            size_hint_y=None,
            height=dp(40)
        )
        
        # buttons
        logout_btn = RoundedButton(
            text='Вийти з акаунту',
            size_hint_y=None,
            height=dp(45),
            bg_color='#D8F3EB',
            text_color=[0.04, 0.25, 0.21, 1]
        )
        
        exit_btn = RoundedButton(
            text='Вихід із програми',
            size_hint_y=None,
            height=dp(45),
            bg_color='#D8F3EB',
            text_color=[0.04, 0.25, 0.21, 1]
        )
        
        # bind button actions
        logout_btn.bind(on_press=lambda x: [popup.dismiss(), self.logout()])
        exit_btn.bind(on_press=lambda x: [popup.dismiss(), self.exit_app()])
        
        # add elements to content
        content.add_widget(title_label)
        content.add_widget(logout_btn)
        content.add_widget(exit_btn)
        
        popup.add_widget(content)
        
        popup.open()

    def on_enter(self):
        """Called when the screen enters the view."""
        super(TransactionsScreen, self).on_enter()
        
        if not self.controller:
            return
        
        if not hasattr(self, '_transactions_loaded') or not self._transactions_loaded:
            transactions = self.controller.get_transactions(force_refresh=False)
            
            if not transactions:
                self.controller.get_transactions(force_refresh=True)
            
            self._transactions_loaded = True
            
            Clock.schedule_once(self._load_transactions, 0.2)

    def logout(self):
        """Log out the current user."""
        from kivy.app import App
        app = App.get_running_app()

        if hasattr(app, 'auth_controller'):
            app.auth_controller.logout()
        
        # Переходимо на first_screen
        self.switch_screen('first_screen', 'right')
    
    def exit_app(self):
        """Exit the application."""
        from kivy.core.window import Window
        Window.close()
    
    def _update_rect(self, instance, value):
        """Update content rectangle when size or position changes."""
        if hasattr(self, 'content_rect'):
            self.content_rect.pos = instance.pos
            self.content_rect.size = instance.size