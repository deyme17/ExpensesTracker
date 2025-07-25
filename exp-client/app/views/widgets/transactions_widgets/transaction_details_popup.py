from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp, sp
from kivy.animation import Animation
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from kivy.uix.scrollview import ScrollView

from app.utils.language_mapper import LanguageMapper as LM
from app.utils.formatters import format_date
from app.utils.constants import INCOME
from app.views.widgets.buttons.styled_button import RoundedButton


class TransactionDetailsPopup(ModalView):
    """
    Modal popup displaying detailed transaction information with edit/delete actions.
    Args:
        transaction: Transaction object to display
        meta_data_controller: Provides category/currency name resolution
        on_edit: Callback for edit action
        on_delete: Callback for delete action
    """
    def __init__(self, transaction, meta_data_controller, on_edit, on_delete, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.8, 0.7)
        self.background = ''
        self.background_color = (0, 0, 0, 0)
        self.overlay_color = (0, 0, 0, 0.6)

        self.transaction = transaction
        self.meta_data_controller = meta_data_controller

        self.on_edit = on_edit
        self.on_delete = on_delete

        self.build_ui()

    def build_ui(self):
        content = BoxLayout(
            orientation="vertical",
            spacing=dp(12),
            padding=[dp(20), dp(10), dp(20), dp(20)],
            opacity=0
        )
        with content.canvas.before:
            Color(rgba=get_color_from_hex('#0A4035'))
            self._bg_rect = RoundedRectangle(size=content.size, pos=content.pos, radius=[dp(15)])
        content.bind(size=self._update_bg, pos=self._update_bg)

        title = Label(
            text=LM.message("transaction_details_title"),
            font_size=sp(20),
            bold=True,
            color=get_color_from_hex('#FFFFFF'),
            size_hint_y=None,
            height=dp(40),
            halign="center",
            valign="middle"
        )
        title.bind(size=lambda inst, val: setattr(inst, "text_size", (inst.width, inst.height)))
        content.add_widget(title)

        scroll = ScrollView(size_hint=(1, 1))
        details_layout = BoxLayout(
            orientation="vertical",
            spacing=dp(10),
            size_hint_y=None,
            padding=[0, 0, 0, dp(10)]
        )
        details_layout.bind(minimum_height=details_layout.setter("height"))

        def add_detail(label_key, value_text):
            row = BoxLayout(size_hint_y=None, height=dp(32), spacing=dp(12))
            lbl = Label(
                text=f"{LM.field_name(label_key)}:",
                font_size=sp(16),
                color=get_color_from_hex('#FFFFFF'),
                size_hint_x=0.35,
                halign="left",
                valign="middle"
            )
            lbl.bind(size=lambda inst, val: setattr(inst, "text_size", (inst.width, inst.height)))
            val = Label(
                text=str(value_text),
                font_size=sp(16),
                color=get_color_from_hex('#D8F3EB'),
                size_hint_x=0.40,
                halign="left",
                valign="middle"
            )
            val.bind(size=lambda inst, val: setattr(inst, "text_size", (inst.width, inst.height)))
            row.add_widget(lbl)
            row.add_widget(val)
            return row

        t = self.transaction

        category_name = self.meta_data_controller.get_category_name_by_mcc(t.mcc_code)
        currency_name = self.meta_data_controller.get_currency_name_by_code(t.currency_code)

        details_layout.add_widget(add_detail("category", LM.category(category_name)))

        try:
            amt = abs(float(t.amount))
            sign = "+" if t.type == INCOME else "-"
            amt_text = f"{sign}{amt:,.2f} ({currency_name})"
        except Exception:
            amt_text = f"{t.amount} ({currency_name})"

        details_layout.add_widget(add_detail("amount", amt_text))
        details_layout.add_widget(add_detail("date", format_date(t.date)))
        details_layout.add_widget(add_detail("payment_method", LM.payment_method(t.payment_method)))

        try:
            cb = float(t.cashback)
            if cb > 0:
                details_layout.add_widget(add_detail("cashback", cb))
        except Exception:
            pass

        try:
            cm = float(t.commission)
            if cm > 0:
                details_layout.add_widget(add_detail("commission", cm))
        except Exception:
            pass

        if t.description and t.description.strip():
            desc_lbl = Label(
                text=LM.field_name("description") + ":",
                font_size=sp(16),
                color=get_color_from_hex('#FFFFFF'),
                size_hint_y=None,
                height=dp(32),
                halign="left",
                valign="middle"
            )
            desc_lbl.bind(size=lambda inst, val: setattr(inst, "text_size", (inst.width, inst.height)))
            details_layout.add_widget(desc_lbl)

            desc_text = Label(
                text=t.description,
                font_size=sp(16),
                color=get_color_from_hex('#D8F3EB'),
                size_hint_y=None,
                height=dp(60),
                halign="center",
                valign="middle"
            )
            desc_text.bind(size=lambda inst, val: setattr(inst, "text_size", (inst.width, inst.height)))
            details_layout.add_widget(desc_text)

        scroll.add_widget(details_layout)
        content.add_widget(scroll)

        btn_box = BoxLayout(size_hint_y=None, height=dp(48), spacing=dp(10))
        btn_edit = RoundedButton(text=LM.message("edit_button"), bg_color='#0F7055', font_size=sp(13))
        btn_delete = RoundedButton(text=LM.message("delete_button"), bg_color='#F44336', font_size=sp(13))
        btn_close = RoundedButton(text=LM.message("close_button"), bg_color='#445555', font_size=sp(13))
        btn_edit.bind(on_press=lambda inst: (self.dismiss(), self.on_edit()))
        btn_delete.bind(on_press=lambda inst: (self.dismiss(), self.on_delete()))
        btn_close.bind(on_press=lambda inst: self.dismiss())
        btn_box.add_widget(btn_edit)
        btn_box.add_widget(btn_delete)
        btn_box.add_widget(btn_close)
        content.add_widget(btn_box)

        self.add_widget(content)
        Animation(opacity=1, d=0.3).start(content)

    def _update_bg(self, instance, value):
        self._bg_rect.pos = instance.pos
        self._bg_rect.size = instance.size
