from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ObjectProperty
from datetime import datetime

from app.utils.language_mapper import LanguageMapper as LM
from app.views.widgets.inputs.date_input import LabeledDateInput
from app.views.widgets.inputs.custom_spinner import LabeledSpinner
from app.views.widgets.buttons.styled_button import RoundedButton
from app.utils.theme import get_primary_color, get_text_primary_color
from app.utils.constants import TRANSACTION_TYPES

import traceback


class AnalyticsFilterPopup(ModalView):
    """
    A simplified popup for analytics filtering: date interval and transaction type only.
    """
    on_apply = ObjectProperty(None)
    on_reset = ObjectProperty(None)

    def __init__(self, *, filter_state, on_apply=None, on_reset=None, **kwargs):
        super().__init__(**kwargs)
        self.filter_state = filter_state
        self.on_apply = on_apply
        self.on_reset = on_reset

        self.size_hint = (0.85, 0.65)
        self.auto_dismiss = False
        self.background = ""
        self.background_color = (0, 0, 0, 0)
        self.overlay_color = (0, 0, 0, 0.7)

        Clock.schedule_once(lambda dt: self._build_ui(), 0)

    def _build_ui(self):
        self.content = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=dp(20),
            opacity=0
        )

        with self.content.canvas.before:
            Color(rgba=get_primary_color())
            self.bg_rect = RoundedRectangle(size=self.content.size, pos=self.content.pos, radius=[dp(20)])
        self.content.bind(size=self._update_rect, pos=self._update_rect)

        title = Label(
            text=LM.message("filter_title"),
            font_size=sp(22),
            bold=True,
            color=get_text_primary_color(),
            size_hint_y=None,
            height=dp(50),
            halign="center"
        )
        title.bind(size=lambda inst, val: setattr(inst, "text_size", (inst.width, None)))
        self.content.add_widget(title)

        # date
        self.start_date_input = LabeledDateInput(label_text=LM.message("start_date_label"))
        self.start_date_input.date_text = self.filter_state.start_date.strftime("%d.%m.%Y")
        self.content.add_widget(self.start_date_input)

        self.end_date_input = LabeledDateInput(label_text=LM.message("end_date_label"))
        self.end_date_input.date_text = self.filter_state.end_date.strftime("%d.%m.%Y")
        self.content.add_widget(self.end_date_input)

        # type
        self.type_spinner = LabeledSpinner(
            label_text=LM.message("transaction_type_label"),
            values=TRANSACTION_TYPES,
            selected=self.filter_state.current_type,
            displayed_value=lambda val: LM.transaction_type(val)
        )
        self.content.add_widget(self.type_spinner)

        self.content.add_widget(BoxLayout(size_hint_y=1))

        # buttons
        btn_box = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))
        close_btn = RoundedButton(text=LM.message("close_button"), bg_color="#666666", font_size=sp(14))
        apply_btn = RoundedButton(text=LM.message("apply_button"), bg_color="#0F7055", font_size=sp(14))

        close_btn.bind(on_press=lambda *a: self.dismiss())
        apply_btn.bind(on_press=self._apply_fields)

        btn_box.add_widget(close_btn)
        btn_box.add_widget(apply_btn)
        self.content.add_widget(btn_box)

        self.add_widget(self.content)
        Animation(opacity=1, d=0.3).start(self.content)

    def _apply_fields(self, *args):
        try:
            sd, sm, sy = self.start_date_input.date_text.split(".")
            ed, em, ey = self.end_date_input.date_text.split(".")
            start_date = datetime(int(sy), int(sm), int(sd))
            end_date = datetime(int(ey), int(em), int(ed))
            transaction_type = self.type_spinner.selected

            # state update
            self.filter_state.update(
                current_type=transaction_type,
                start_date=start_date,
                end_date=end_date
            )

            if self.on_apply:
                self.on_apply(
                    current_type=transaction_type,
                    start_date=start_date,
                    end_date=end_date
                )
            self.dismiss()

        except Exception:
            traceback.print_exc()
            self._show_temp_error(LM.server_error("unknown_error"))

    def _show_temp_error(self, text: str):
        label = Label(
            text=text,
            color=(1, 0.3, 0.3, 1),
            font_size=sp(14),
            size_hint_y=None,
            height=dp(20)
        )
        self.content.add_widget(label, index=0)
        Clock.schedule_once(lambda dt: self.content.remove_widget(label), 2)

    def _update_rect(self, instance, value):
        if hasattr(self, "bg_rect"):
            self.bg_rect.pos = instance.pos
            self.bg_rect.size = instance.size
