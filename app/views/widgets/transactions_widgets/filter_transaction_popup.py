from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ObjectProperty
from datetime import datetime, timedelta

from app.views.widgets.inputs.date_input import LabeledDateInput
from app.views.widgets.inputs.styled_text_input import LabeledInput
from app.views.widgets.inputs.custom_spinner import LabeledSpinner
from app.views.widgets.buttons.styled_button import RoundedButton
from app.utils.constants import (
    TRANSACTION_TYPE_ALL, TRANSACTION_TYPE_INCOME, TRANSACTION_TYPE_EXPENSE,
    PAYMENT_METHOD_ALL, PAYMENT_METHOD_CARD, PAYMENT_METHOD_CASH
)
from app.utils.theme import get_primary_color, get_text_primary_color
from app.utils.validators import validate_date


class FilterPopup(ModalView):
    """
    Modal window for filtration of transactions.
    Repeats logic and ui from the initial implementation of Show_filter.
    """
    on_apply = ObjectProperty(None)
    on_reset = ObjectProperty(None)

    def __init__(self, **kwargs):
        super(FilterPopup, self).__init__(**kwargs)
        self.size_hint = (0.85, 0.9)
        self.auto_dismiss = False
        self.background = ''
        self.background_color = (0, 0, 0, 0)
        self.overlay_color = (0, 0, 0, 0.7)
        self.build_ui()

    def build_ui(self):
        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True, size_hint=(1, 1))
        content = BoxLayout(
            orientation='vertical',
            spacing=dp(12),
            padding=dp(20),
            size_hint_y=None,
            opacity=0
        )
        content.bind(minimum_height=content.setter('height'))

        with content.canvas.before:
            Color(rgba=get_primary_color())
            self.bg_rect = RoundedRectangle(size=content.size, pos=content.pos, radius=[dp(20)])
        content.bind(
            size=lambda inst, val: setattr(self.bg_rect, 'size', val),
            pos=lambda inst, val: setattr(self.bg_rect, 'pos', inst.pos)
        )

        # title
        title = Label(
            text='Фільтр транзакцій',
            font_size=sp(22),
            bold=True,
            color=get_text_primary_color(),
            halign='center',
            size_hint_y=None,
            height=dp(50)
        )
        title.bind(size=lambda inst, val: setattr(inst, 'text_size', (inst.width, None)))
        content.add_widget(title)

        # sum
        self.min_amount = LabeledInput(label_text='Сума від:', hint_text='0', text='0')
        self.max_amount = LabeledInput(label_text='Сума до:', hint_text='1000000', text='1000000')
        content.add_widget(self.min_amount)
        content.add_widget(self.max_amount)

        # date
        self.start_date = LabeledDateInput(label_text='Початкова дата:')
        year_ago = datetime.now() - timedelta(days=365)
        self.start_date.date_text = year_ago.strftime('%d.%m.%Y')
        self.end_date = LabeledDateInput(label_text='Кінцева дата:')
        self.end_date.date_text = datetime.now().strftime('%d.%m.%Y')
        content.add_widget(self.start_date)
        content.add_widget(self.end_date)

        # type
        self.type_spinner = LabeledSpinner(
            label_text='Тип транзакції:',
            values=[TRANSACTION_TYPE_ALL, TRANSACTION_TYPE_INCOME, TRANSACTION_TYPE_EXPENSE],
            selected=TRANSACTION_TYPE_ALL
        )
        content.add_widget(self.type_spinner)

        # method
        self.payment_spinner = LabeledSpinner(
            label_text='Спосіб оплати:',
            values=[PAYMENT_METHOD_ALL, PAYMENT_METHOD_CARD, PAYMENT_METHOD_CASH],
            selected=PAYMENT_METHOD_ALL
        )
        content.add_widget(self.payment_spinner)

        # space
        content.add_widget(BoxLayout(size_hint_y=1))

        # buttons
        btn_box = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        reset_btn = RoundedButton(text='Скинути', bg_color='#445555', font_size=sp(14))
        close_btn = RoundedButton(text='Закрити', bg_color='#666666', font_size=sp(14))
        apply_btn = RoundedButton(text='Застосувати', bg_color='#0F7055', font_size=sp(14))

        reset_btn.bind(on_press=self._reset_fields)
        close_btn.bind(on_press=lambda *a: self.dismiss())
        apply_btn.bind(on_press=self._apply_fields)

        btn_box.add_widget(reset_btn)
        btn_box.add_widget(close_btn)
        btn_box.add_widget(apply_btn)
        content.add_widget(btn_box)

        scroll.add_widget(content)
        self.add_widget(scroll)
        self.open()
        Animation(opacity=1, d=0.3).start(content)

    def _reset_fields(self, *args):
        now = datetime.now()
        self.min_amount.text = '0'
        self.max_amount.text = '1000000'
        year_ago = now - timedelta(days=365)
        self.start_date.date_text = year_ago.strftime('%d.%m.%Y')
        self.end_date.date_text = now.strftime('%d.%m.%Y')
        self.type_spinner.selected = TRANSACTION_TYPE_ALL
        self.payment_spinner.selected = PAYMENT_METHOD_ALL
        if self.on_reset:
            self.on_reset()

    def _apply_fields(self, *args):
        try:
            min_val = float(self.min_amount.text.replace(',', '.'))
            max_val = float(self.max_amount.text.replace(',', '.'))
            sd, sm, sy = self.start_date.date_text.split('.')
            ed, em, ey = self.end_date.date_text.split('.')
            start_ok, start_dt = validate_date(f"{sd}.{sm}.{sy}")
            end_ok, end_dt = validate_date(f"{ed}.{em}.{ey}")
            if not start_ok:
                start_dt = datetime.now() - timedelta(days=365)
            if not end_ok:
                end_dt = datetime.now()

            inc = None
            if self.type_spinner.selected == TRANSACTION_TYPE_INCOME:
                inc = True
            elif self.type_spinner.selected == TRANSACTION_TYPE_EXPENSE:
                inc = False

            pay = None if self.payment_spinner.selected == PAYMENT_METHOD_ALL else self.payment_spinner.selected

            if self.on_apply:
                self.on_apply(
                    min_amount=min_val,
                    max_amount=max_val,
                    start_date=start_dt,
                    end_date=end_dt,
                    is_income=inc,
                    payment_method=pay
                )
            self.dismiss()
        except Exception as e:
            print(f"Filter error: {e}")
