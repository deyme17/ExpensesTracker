from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView
from kivy.metrics import dp, sp
from kivy.properties import ListProperty, ObjectProperty
from kivy.graphics import Color, RoundedRectangle

from utils.language_mapper import LanguageMapper as LM
from app.utils.theme import get_primary_color, get_text_primary_color
from app.views.widgets.buttons.styled_button import RoundedButton


class AccountSelectPopup(ModalView):
    accounts = ListProperty()
    on_account_selected = ObjectProperty(None)

    def __init__(self, accounts, on_account_selected=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.8, 0.60)
        self.background = ''
        self.background_color = (0, 0, 0, 0)
        self.overlay_color = (0, 0, 0, 0.7)
        self.auto_dismiss = False

        self.accounts = accounts
        self.on_account_selected = on_account_selected
        self.selected_account_id = None
        self.account_buttons = []

        self._build_content()

    def _build_content(self):
        main_box = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(20))

        with main_box.canvas.before:
            Color(rgba=get_primary_color())
            self.bg_rect = RoundedRectangle(size=main_box.size, pos=main_box.pos, radius=[dp(20)])
        main_box.bind(size=self._update_bg, pos=self._update_bg)

        title = Label(
            text=LM.message("choose_account"),
            font_size=sp(22),
            bold=True,
            color=get_text_primary_color(),
            size_hint_y=None,
            height=dp(50)
        )
        main_box.add_widget(title)

        content = BoxLayout(orientation='vertical', size_hint=(1, 1))
        if not self.accounts:
            no_accounts = Label(
                text=LM.message("now_available_acc"),
                font_size=sp(18),
                color=get_text_primary_color(),
                size_hint=(1, 1)
            )
            content.add_widget(no_accounts)
        else:
            scroll = ScrollView(size_hint=(1, 1))
            accounts_box = BoxLayout(orientation='vertical', size_hint_y=None, spacing=dp(10))
            accounts_box.bind(minimum_height=accounts_box.setter('height'))

            for acc in self.accounts:
                acc_str = f"{acc.currency_code}-{acc.type}"
                btn = RoundedButton(
                    text=acc_str,
                    size_hint_y=None,
                    height=dp(50),
                    bg_color="#D8F3EB",
                    text_color=[0.04, 0.25, 0.21, 1]
                )
                btn.bind(on_press=lambda btn, acc_id=acc.account_id: self._select_account(acc_id, btn))
                self.account_buttons.append(btn)
                accounts_box.add_widget(btn)

            scroll.add_widget(accounts_box)
            content.add_widget(scroll)

        main_box.add_widget(content)

        # buttons
        self.btn_box = BoxLayout(size_hint_y=None, height=dp(50), spacing=dp(10))

        close_btn = RoundedButton(
            text=LM.message("close_button"),
            bg_color='#666666',
            text_color=[1, 1, 1, 1]
        )
        close_btn.bind(on_press=lambda *a: self.dismiss())

        self.save_btn = RoundedButton(
            text=LM.message("save_button"),
            bg_color='#0F7055',
            text_color=[1, 1, 1, 1],
            disabled=True
        )
        self.save_btn.bind(on_press=self._save_selection)

        self.btn_box.add_widget(close_btn)
        self.btn_box.add_widget(self.save_btn)
        main_box.add_widget(self.btn_box)

        self.add_widget(main_box)

    def _update_bg(self, instance, value):
        self.bg_rect.pos = instance.pos
        self.bg_rect.size = instance.size

    def _select_account(self, account_id, selected_btn):
        self.selected_account_id = account_id
        self.save_btn.disabled = False

        for btn in self.account_buttons:
            btn.bg_color = "#D8F3EB"
        selected_btn.bg_color = "#B2DFDB"

    def _save_selection(self, *args):
        if self.selected_account_id and self.on_account_selected:
            self.on_account_selected(self.selected_account_id)
        self.dismiss()