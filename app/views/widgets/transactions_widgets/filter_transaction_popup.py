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

from app.utils.theme import get_primary_color, get_text_primary_color
from app.utils.validators import validate_date
from app.utils.language_mapper import LanguageMapper as LM
from app.utils.constants import TRANSACTION_TYPES, PAYMENT_METHODS, ALL
from kivy.app import App


class FilterPopup(ModalView):
    on_apply = ObjectProperty(None)
    on_reset = ObjectProperty(None)

    def __init__(self, *, start_date=None, end_date=None, on_apply=None, on_reset=None,
                 min_amount="0", max_amount="1000000", type_selected="all",
                 category_selected="all", payment_selected="all", **kwargs):
        super().__init__(**kwargs)
        self.on_apply = on_apply
        self.on_reset = on_reset
        self.start_date_val = start_date
        self.end_date_val = end_date
        self.min_amount_val = min_amount
        self.max_amount_val = max_amount
        self.type_selected = type_selected
        self.category_selected = category_selected
        self.payment_selected = payment_selected

        self.size_hint = (0.85, 0.9)
        self.auto_dismiss = False
        self.background = ''
        self.background_color = (0, 0, 0, 0)
        self.overlay_color = (0, 0, 0, 0.7)

        now = datetime.now()
        self._initial_start = start_date or (now - timedelta(days=365))
        self._initial_end = end_date or now

        self.build_ui()

    def build_ui(self):
        scroll = ScrollView(do_scroll_x=False, do_scroll_y=True, size_hint=(1, 1))
        content = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(20),
            size_hint_y=None,
            opacity=0
        )
        content.bind(minimum_height=content.setter("height"))

        with content.canvas.before:
            Color(rgba=get_primary_color())
            self.bg_rect = RoundedRectangle(size=content.size, pos=content.pos, radius=[dp(20)])
        content.bind(
            size=lambda inst, val: setattr(self.bg_rect, "size", val),
            pos=lambda inst, val: setattr(self.bg_rect, "pos", inst.pos)
        )

        title = Label(
            text=LM.message("filter_title"),
            font_size=sp(22),
            bold=True,
            color=get_text_primary_color(),
            halign="center",
            size_hint_y=None,
            height=dp(50)
        )
        title.bind(size=lambda inst, val: setattr(inst, "text_size", (inst.width, None)))
        content.add_widget(title)

        self.min_amount = LabeledInput(
            label_text=LM.field_name("amount") + " " + LM.message("from") + ":",
            hint_text="0",
            text=self.min_amount_val
        )
        self.max_amount = LabeledInput(
            label_text=LM.field_name("amount") + " " + LM.message("to") + ":",
            hint_text="1000000",
            text=self.max_amount_val
        )
        content.add_widget(self.min_amount)
        content.add_widget(self.max_amount)

        self.start_date = LabeledDateInput(label_text=LM.message("start_date_label"))
        self.start_date.date_text = self._initial_start.strftime('%d.%m.%Y')
        self.end_date = LabeledDateInput(label_text=LM.message("end_date_label"))
        self.end_date.date_text = self._initial_end.strftime('%d.%m.%Y')
        content.add_widget(self.start_date)
        content.add_widget(self.end_date)

        self.type_spinner = LabeledSpinner(
            label_text=LM.message("transaction_type_label"),
            values=TRANSACTION_TYPES + [ALL],
            selected=self.type_selected,
            displayed_value=LM.transaction_type
        )
        content.add_widget(self.type_spinner)

        # categories/payment method
        static = App.get_running_app().static_data_service

        categories = static.get_categories()
        category_codes = ["all"] + [c.mcc_code for c in categories]
        self.category_spinner = LabeledSpinner(
            label_text=LM.message("category_label"),
            values=category_codes,
            selected=self.category_selected,
            displayed_value=lambda code: LM.category(static.get_category_name_by_mcc(code)) if code != "all" else "Усі"
        )

        self.payment_spinner = LabeledSpinner(
            label_text=LM.message("payment_method_label"),
            values=PAYMENT_METHODS + [ALL],
            selected=self.payment_selected,
            displayed_value=LM.payment_method
        )

        content.add_widget(self.payment_spinner)

        content.add_widget(BoxLayout(size_hint_y=1))

        btn_box = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        reset_btn = RoundedButton(text=LM.message("reset_button"), bg_color='#445555', font_size=sp(14))
        close_btn = RoundedButton(text=LM.message("close_button"), bg_color='#666666', font_size=sp(14))
        apply_btn = RoundedButton(text=LM.message("apply_button"), bg_color='#0F7055', font_size=sp(14))

        reset_btn.bind(on_press=self._reset_fields)
        close_btn.bind(on_press=lambda *a: self.dismiss())
        apply_btn.bind(on_press=self._apply_fields)

        btn_box.add_widget(reset_btn)
        btn_box.add_widget(close_btn)
        btn_box.add_widget(apply_btn)
        content.add_widget(btn_box)

        scroll.add_widget(content)
        self.add_widget(scroll)
        Animation(opacity=1, d=0.3).start(content)

    def _reset_fields(self, *args):
        now = datetime.now()
        self.min_amount.text = "0"
        self.max_amount.text = "1000000"
        year_ago = now - timedelta(days=365)
        self.start_date.date_text = year_ago.strftime('%d.%m.%Y')
        self.end_date.date_text = now.strftime('%d.%m.%Y')
        self.type_spinner.selected = "all"
        self.payment_spinner.selected = "all"
        self.category_spinner.selected = "all"
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

            ttype = None if self.type_spinner.selected == "all" else self.type_spinner.selected
            pay = None if self.payment_spinner.selected == "all" else self.payment_spinner.selected

            # category
            category = None
            if self.category_spinner.selected != "all":
                static = App.get_running_app().static_data_service
                selected_name = self.category_spinner.selected
                for c in static.get_categories():
                    if c.name == selected_name:
                        category = c.mcc_code
                        break

            if self.on_apply:
                self.on_apply(
                    min_amount=min_val,
                    max_amount=max_val,
                    start_date=start_dt,
                    end_date=end_dt,
                    type=ttype,
                    payment_method=pay,
                    category=category
                )
            self.dismiss()
        except Exception as e:
            print(f"Filter error: {e}")
