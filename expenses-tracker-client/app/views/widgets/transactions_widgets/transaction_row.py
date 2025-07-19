from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.properties import StringProperty, ObjectProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.metrics import dp, sp

from app.utils.theme import (
    get_income_color, get_expense_color, get_text_primary_color
)
from app.utils.formatters import format_amount
from app.utils.constants import INCOME, CARD
from app.utils.language_mapper import LanguageMapper as LM


class TransactionRow(BoxLayout):
    """
    Custom row widget for displaying transaction items in a list.
    Properties:
        transaction_id: Unique transaction identifier
        category: Transaction category name
        currency: Currency code
        amount: Formatted amount string  
        date: Transaction date string
        type: Transaction type (income/expense)
        payment_method: Payment method type
        description: Transaction description
        cashback: Cashback amount
        commission: Commission amount
        controller: Reference to transaction controller
        transactions_screen: Parent screen reference
    """
    transaction_id = StringProperty('')
    category = StringProperty('')
    currency = StringProperty('')
    amount = StringProperty('')
    date = StringProperty('')
    type = StringProperty('')
    payment_method = StringProperty(CARD)
    description = StringProperty('')
    cashback = StringProperty('0')
    commission = StringProperty('0')
    controller = ObjectProperty(None)
    transactions_screen = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(TransactionRow, self).__init__(**kwargs)
        self.orientation = 'horizontal'
        self.size_hint_y = None
        self.height = dp(60)
        self.padding = [dp(10), dp(5), dp(10), dp(5)]
        self.spacing = dp(10)
        self._build_ui()

    def _build_ui(self):
        self.clear_widgets()

        with self.canvas.before:
            color = get_income_color(0.85) if self.type == INCOME else get_expense_color(0.85)
            self.background_color = Color(*color)
            self.background_rect = RoundedRectangle(
                pos=self.pos,
                size=self.size,
                radius=[dp(8)]
            )

        self.bind(pos=self._update_rect, size=self._update_rect)

        info_layout = BoxLayout(
            orientation='vertical',
            size_hint_x=0.5,
            spacing=dp(2)
        )

        category_label = Label(
            text=LM.category(self.category),
            font_size=sp(16),
            bold=True,
            color=get_text_primary_color(),
            halign='left',
            valign='middle',
            size_hint_y=0.6,
            text_size=(None, None)
        )

        date_label = Label(
            text=self.date,
            font_size=sp(12),
            color=get_text_primary_color(0.8),
            halign='left',
            valign='middle',
            size_hint_y=0.4,
            text_size=(None, None)
        )

        info_layout.add_widget(category_label)
        info_layout.add_widget(date_label)

        amount_layout = BoxLayout(
            orientation='vertical',
            size_hint_x=0.4,
            spacing=dp(2)
        )

        try:
            amount_value = float(self.amount.replace(',', '.').replace('+', '').replace('-', ''))
            formatted_amount = format_amount(
                amount_value if self.type == INCOME else -amount_value,
                self.currency,
                show_sign=True
            )
        except ValueError:
            formatted_amount = self.amount

        amount_label = Label(
            text=formatted_amount,
            font_size=sp(15),
            bold=True,
            color='white',
            halign='right',
            valign='middle',
            size_hint_y=1.0,
            text_size=(None, None)
        )

        amount_layout.add_widget(amount_label)

        self.add_widget(info_layout)
        self.add_widget(amount_layout)

    def _update_rect(self, instance, value):
        if hasattr(self, 'background_rect'):
            self.background_rect.pos = instance.pos
            self.background_rect.size = instance.size
                
    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            if self.transactions_screen:
                self.transactions_screen.show_transaction_details(self.transaction_id)
                return True
        return super(TransactionRow, self).on_touch_down(touch)
