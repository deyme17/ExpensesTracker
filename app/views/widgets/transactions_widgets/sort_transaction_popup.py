from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.widget import Widget
from kivy.properties import ObjectProperty, ListProperty, StringProperty, BooleanProperty
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle
from kivy.animation import Animation

from app.views.widgets.inputs.custom_spinner import CustomSpinner
from app.views.widgets.buttons.styled_button import RoundedButton
from app.utils.theme import get_primary_color, get_text_primary_color


class SortPopup(ModalView):
    on_sort = ObjectProperty(None)  # callable(field: str, ascending: bool)

    sort_fields = ListProperty(['Дата', 'Сума', 'Кешбек', 'Комісія'])
    selected_field = StringProperty('Дата')
    ascending = BooleanProperty(True)

    def __init__(self, **kwargs):
        super(SortPopup, self).__init__(**kwargs)
        self.size_hint = (0.85, 0.6)
        self.auto_dismiss = False
        self.background = ''
        self.background_color = (0, 0, 0, 0)
        self.overlay_color = (0, 0, 0, 0.7)

        self.build_ui()

    def build_ui(self):
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

        # Title
        title_label = Label(
            text='Сортування транзакцій',
            font_size=sp(22),
            bold=True,
            color=get_text_primary_color(),
            halign='center',
            size_hint_y=None,
            height=dp(50)
        )

        # Sort by field
        field_label = Label(
            text='Сортувати за:',
            font_size=sp(16),
            color=get_text_primary_color(),
            size_hint_y=None,
            height=dp(30)
        )

        self.field_spinner = CustomSpinner(
            text=self.selected_field,
            values=self.sort_fields,
            size_hint_y=None,
            height=dp(45)
        )

        # Direction
        direction_label = Label(
            text='Напрямок:',
            font_size=sp(16),
            color=get_text_primary_color(),
            size_hint_y=None,
            height=dp(30)
        )

        self.direction_spinner = CustomSpinner(
            text='За зростанням' if self.ascending else 'За спаданням',
            values=['За зростанням', 'За спаданням'],
            size_hint_y=None,
            height=dp(45)
        )

        # Buttons
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

        cancel_button.bind(on_release=lambda x: self.dismiss())
        apply_button.bind(on_release=self._apply_sort)

        buttons_box.add_widget(cancel_button)
        buttons_box.add_widget(apply_button)

        content.add_widget(title_label)
        content.add_widget(field_label)
        content.add_widget(self.field_spinner)
        content.add_widget(direction_label)
        content.add_widget(self.direction_spinner)
        content.add_widget(Widget())
        content.add_widget(buttons_box)

        self.add_widget(content)
        Animation(opacity=1, d=0.3).start(content)

    def _apply_sort(self, *args):
        if self.on_sort:
            ascending = self.direction_spinner.text == 'За зростанням'
            self.on_sort(self.field_spinner.text, ascending)
        self.dismiss()

    def _update_rect(self, instance, value):
        self.content_rect.pos = instance.pos
        self.content_rect.size = instance.size
