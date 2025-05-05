from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle
from app.views.widgets.buttons.styled_button import RoundedButton
from app.utils.theme import get_primary_color, get_text_primary_color


class MenuPopup(ModalView):
    """
    Put the modal menu with actions: get out of the account, get out of the program.
    """
    def __init__(self, on_logout=None, on_exit=None, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.7, 0.25)
        self.background = ''
        self.background_color = (0, 0, 0, 0)
        self.overlay_color = (0, 0, 0, 0.7)
        self.on_logout = on_logout
        self.on_exit = on_exit
        self._build_content()

    def _build_content(self):
        content = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
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

        logout_btn.bind(on_press=lambda x: [self.dismiss(), self.on_logout() if self.on_logout else None])
        exit_btn.bind(on_press=lambda x: [self.dismiss(), self.on_exit() if self.on_exit else None])

        content.add_widget(title_label)
        content.add_widget(logout_btn)
        content.add_widget(exit_btn)

        self.add_widget(content)

    def _update_rect(self, instance, value):
        if hasattr(self, 'content_rect'):
            self.content_rect.pos = instance.pos
            self.content_rect.size = instance.size