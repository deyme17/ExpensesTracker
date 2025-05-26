from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle
from kivy.app import App
from kivy.properties import ObjectProperty
from datetime import datetime
from kivy.clock import Clock

from app.views.widgets.inputs.date_input import LabeledDateInput
from app.views.widgets.inputs.styled_text_input import LabeledInput
from app.views.widgets.inputs.custom_spinner import LabeledSpinner
from app.views.widgets.buttons.styled_button import RoundedButton

from app.utils.language_mapper import LanguageMapper as LM
from app.utils.theme import get_color_from_hex, get_text_primary_color
from app.utils.formatters import format_date
from app.utils.constants import PAYMENT_METHODS, INCOME, DEFAULT_CURRENCY

class AddTransactionPopup(ModalView):
    type = ObjectProperty(None)
    on_save = ObjectProperty(None)
    existing_transaction = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.9, 0.9)
        self.background = ''
        self.background_color = (0, 0, 0, 0)
        self.overlay_color = (0, 0, 0, 0.7)
        self.on_save = kwargs.get("on_save")
        self.build_ui()

        if self.existing_transaction:
            self._fill_fields_with_existing_transaction()

    def build_ui(self):
        static = App.get_running_app().static_data_service

        self.content = BoxLayout(orientation="vertical", spacing=dp(15), padding=dp(20), opacity=0)

        with self.content.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            self.bg_rect = RoundedRectangle(size=self.content.size, pos=self.content.pos, radius=[dp(15)])

        self.content.bind(size=self._update_bg, pos=self._update_bg)

        title_text = (
            LM.message("edit_transaction") if self.existing_transaction
            else (LM.message("add_income") if self.type == INCOME else LM.message("add_expense"))
        )
                      
        title = Label(text=title_text, font_size=sp(20), bold=True, color=get_text_primary_color(),
                      halign="center", size_hint_y=None, height=dp(40))

        scroll = ScrollView()
        fields_container = BoxLayout(orientation="vertical", spacing=dp(10), size_hint_y=None)
        fields_container.bind(minimum_height=fields_container.setter("height"))

        # Load static data
        categories = static.get_categories()
        name_to_mcc = {c.name: str(c.mcc_code) for c in categories}
        self.name_to_mcc = name_to_mcc

        currencies = static.get_currencies()
        name_to_currency = {c.name: str(c.currency_code) for c in currencies}
        self.name_to_currency = name_to_currency

        selected_category = (
            next((name for name, mcc in name_to_mcc.items() if str(mcc) == str(self.existing_transaction.mcc_code)),
                 list(name_to_mcc.keys())[0])
            if self.existing_transaction else list(name_to_mcc.keys())[0]
        )

        selected_currency = (
            next((name for name, code in name_to_currency.items() if str(code) == str(self.existing_transaction.currency_code)),
                 list(name_to_currency.keys())[0])
            if self.existing_transaction else list(name_to_currency.keys())[0]
        )

        self.category_input = LabeledSpinner(
            label_text=LM.field_name("category") + ":",
            values=list(name_to_mcc.keys()),
            selected=selected_category,
            displayed_value=LM.category
        )

        self.payment_input = LabeledSpinner(
            label_text=LM.field_name("payment_method") + ":",
            values=PAYMENT_METHODS,
            selected=self.existing_transaction.payment_method if self.existing_transaction else PAYMENT_METHODS[0],
            displayed_value=LM.payment_method
        )

        self.amount_input = LabeledInput(
            label_text=LM.field_name("amount") + ":",
            hint_text=LM.message("amount_hint")
        )

        self.currency_input = LabeledSpinner(
            label_text=LM.field_name("currency") + ":",
            values=list(name_to_currency.keys()),
            selected=selected_currency,
            displayed_value=lambda name: name
        )

        self.date_input = LabeledDateInput(label_text=LM.field_name("date") + ":")

        self.cashback_input = LabeledInput(
            label_text=LM.field_name("cashback") + ":",
            hint_text=LM.message("cashback_hint"),
            text="0"
        )

        self.commission_input = LabeledInput(
            label_text=LM.field_name("commission") + ":",
            hint_text=LM.message("commission_hint"),
            text="0"
        )

        self.description_input = LabeledInput(
            label_text=LM.field_name("description") + ":",
            hint_text=LM.message("description_hint")
        )

        for widget in [
            self.category_input, self.payment_input, self.amount_input,
            self.currency_input, self.date_input, self.cashback_input,
            self.commission_input, self.description_input
        ]:
            fields_container.add_widget(widget)

        scroll.add_widget(fields_container)

        buttons = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(15))
        cancel_btn = RoundedButton(
            text=LM.message("cancel_button"),
            bg_color='#445555',
            on_press=lambda x: self.dismiss()
        )
        save_btn = RoundedButton(
            text=LM.message("save_button"),
            bg_color='#0F7055',
            on_press=self._save_transaction
        )
        buttons.add_widget(cancel_btn)
        buttons.add_widget(save_btn)

        self.content.add_widget(title)
        self.content.add_widget(scroll)
        self.content.add_widget(buttons)
        self.add_widget(self.content)

        Animation(opacity=1, d=0.3).start(self.content)

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def _save_transaction(self, *args):
        if self.on_save:
            try:
                if not self.amount_input.text.strip():
                    self._show_temp_error(LM.message("amount_required"))
                    return
                data = {
                    "category": self.category_input.selected,
                    "amount": float(self.amount_input.text) if self.type == INCOME else -float(self.amount_input.text),
                    "date": self.date_input.date_text,
                    "description": self.description_input.text,
                    "payment_method": self.payment_input.selected,
                    "currency": self.currency_input.selected,
                    "cashback": self.cashback_input.text,
                    "commission": self.commission_input.text,
                    "transaction_id": self.existing_transaction.transaction_id if self.existing_transaction else None,
                    "popup": self
                }
                self.on_save(**data)
                self.dismiss()
            except Exception as e:
                import traceback
                traceback.print_exc()
        else:
            print("self.on_save is None")

    def _fill_fields_with_existing_transaction(self):
        t = self.existing_transaction

        actual_category_name = next((name for name, mcc in self.name_to_mcc.items() if mcc == str(t.mcc_code)), LM.category("other"))
        actual_currency_name = next((name for name, code in self.name_to_currency.items() if code == str(t.currency_code)), DEFAULT_CURRENCY)

        self.category_input.selected = str(actual_category_name)
        self.payment_input.selected = t.payment_method
        self.amount_input.text = str(abs(t.amount))
        self.currency_input.selected = str(actual_currency_name)
        self.date_input.date_text = format_date(t.date)
        self.cashback_input.text = str(t.cashback)
        self.commission_input.text = str(t.commission)
        self.description_input.text = t.description

    def _show_temp_error(self, text):
        from kivy.uix.label import Label
        label = Label(text=text, color=(1, 0.3, 0.3, 1), font_size=sp(14), size_hint_y=None, height=dp(20))
        self.content.add_widget(label, index=0)
        Clock.schedule_once(lambda dt: self.content.remove_widget(label), 2)
