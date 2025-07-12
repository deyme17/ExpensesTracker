from kivy.uix.modalview import ModalView
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ObjectProperty
from kivy.uix.label import Label
from kivy.clock import Clock

from datetime import datetime, timedelta

from app.views.widgets.inputs.date_input import LabeledDateInput
from app.views.widgets.inputs.styled_text_input import LabeledInput
from app.views.widgets.inputs.custom_spinner import LabeledSpinner
from app.views.widgets.buttons.styled_button import RoundedButton

from app.utils.theme import get_primary_color, get_text_primary_color
from app.utils.validators import validate_date
from app.utils.language_mapper import LanguageMapper as LM
from app.utils.constants import TRANSACTION_TYPES, PAYMENT_METHODS, ALL


class FilterPopup(ModalView):
    """
    Modal dialog for filtering transactions with multiple criteria.
    Args:
        filter_state: Current filter configuration
        on_apply: Apply filters callback
        on_reset: Reset filters callback  
        categories: Available categories for filtering
    """
    on_apply = ObjectProperty(None)
    on_reset = ObjectProperty(None)

    def __init__(self, *, filter_state, on_apply=None, on_reset=None, categories: list, **kwargs):
        super().__init__(**kwargs)
        self.on_apply = on_apply
        self.on_reset = on_reset

        self.category_names = sorted({c.name for c in categories})
        self.filter_state = filter_state

        self.size_hint = (0.85, 0.9)
        self.auto_dismiss = False
        self.background = ''
        self.background_color = (0, 0, 0, 0)
        self.overlay_color = (0, 0, 0, 0.7)

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
        self.content = content
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
            text=self.filter_state.min_amount
        )
        self.max_amount = LabeledInput(
            label_text=LM.field_name("amount") + " " + LM.message("to") + ":",
            hint_text="1000000",
            text=self.filter_state.max_amount
        )
        content.add_widget(self.min_amount)
        content.add_widget(self.max_amount)

        self.start_date = LabeledDateInput(label_text=LM.message("start_date_label"))
        self.start_date.date_text = self.filter_state.start_date.strftime('%d.%m.%Y')
        self.end_date = LabeledDateInput(label_text=LM.message("end_date_label"))
        self.end_date.date_text = self.filter_state.end_date.strftime('%d.%m.%Y')
        content.add_widget(self.start_date)
        content.add_widget(self.end_date)

        self.type_spinner = LabeledSpinner(
            label_text=LM.message("transaction_type_label"),
            values=TRANSACTION_TYPES + [ALL],
            selected=self.filter_state.type_selected,
            displayed_value=LM.transaction_type
        )
        content.add_widget(self.type_spinner)

        category_names = sorted(set(self.category_names))
        category_names.insert(0, ALL)

        self.category_spinner = LabeledSpinner(
            label_text=LM.message("category_label"),
            values=category_names,
            selected=self.filter_state.category_selected,
            displayed_value=LM.category
        )
        content.add_widget(self.category_spinner)

        self.payment_spinner = LabeledSpinner(
            label_text=LM.message("payment_method_label"),
            values=PAYMENT_METHODS + [ALL],
            selected=self.filter_state.payment_selected,
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
        self.filter_state.reset()
        self.dismiss()
        if self.on_reset:
            self.on_reset()

    def _apply_fields(self, *args):
        try:
            min_val = self.min_amount.text.replace(',', '.')
            max_val = self.max_amount.text.replace(',', '.')

            start_ok, start_dt = validate_date(self.start_date.date_text)
            end_ok, end_dt = validate_date(self.end_date.date_text)
            if not start_ok:
                start_dt = datetime.now() - timedelta(days=365)
            if not end_ok:
                end_dt = datetime.now()

            self.filter_state.min_amount = min_val
            self.filter_state.max_amount = max_val
            self.filter_state.start_date = start_dt
            self.filter_state.end_date = end_dt
            self.filter_state.type_selected = self.type_spinner.selected
            self.filter_state.payment_selected = self.payment_spinner.selected
            self.filter_state.category_selected = self.category_spinner.selected

            if self.on_apply:
                self.on_apply(
                    min_amount=min_val,
                    max_amount=max_val,
                    start_date=start_dt,
                    end_date=end_dt,
                    type=None if self.type_spinner.selected == ALL else self.type_spinner.selected,
                    payment_method=None if self.payment_spinner.selected == ALL else self.payment_spinner.selected,
                    category=None if self.category_spinner.selected == ALL else self.category_spinner.selected,
                )
            self.dismiss()
        except Exception as e:
            import traceback
            traceback.print_exc()
            self._show_temp_error(LM.server_error("unknown_error"))

    def _show_temp_error(self, text):
        label = Label(
            text=text,
            color=(1, 0.3, 0.3, 1),
            font_size=sp(14),
            size_hint_y=None,
            height=dp(20)
        )
        self.content.add_widget(label, index=0)
        Clock.schedule_once(lambda dt: self.content.remove_widget(label), 2)