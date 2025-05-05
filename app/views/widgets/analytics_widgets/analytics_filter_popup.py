from kivy.uix.modalview import ModalView
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.metrics import dp, sp
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import StringProperty, ObjectProperty
from datetime import datetime

from app.views.widgets.inputs.custom_spinner import CustomSpinner
from app.views.widgets.buttons.styled_button import RoundedButton
from app.utils.theme import get_primary_color, get_text_primary_color

class AnalyticsFilterPopup(ModalView):
    current_type = StringProperty("Витрати")
    start_date = ObjectProperty()
    end_date = ObjectProperty()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.size_hint = (0.8, 0.8)
        self.background = ''
        self.background_color = (0, 0, 0, 0)
        self.overlay_color = (0, 0, 0, 0.7)

        now = datetime.now()
        self.start_date = datetime(now.year - 1, 1, 1)
        self.end_date = now

        self._build_content()

    def _build_content(self):
        self.content = BoxLayout(orientation='vertical', spacing=dp(15), padding=dp(15), opacity=0)

        with self.content.canvas.before:
            Color(rgba=get_primary_color())
            self.bg_rect = RoundedRectangle(size=self.content.size, pos=self.content.pos, radius=[dp(20)])
        self.content.bind(size=self._update_rect, pos=self._update_rect)

        # title
        self.content.add_widget(Label(
            text='Фільтр транзакцій', font_size=sp(20), bold=True,
            color=get_text_primary_color(), size_hint_y=None, height=dp(40)))

        # type
        self.type_spinner = CustomSpinner(
            text=self.current_type, values=['Витрати', 'Доходи'],
            size_hint_y=None, height=dp(45), padding_x=dp(25))
        self.content.add_widget(Label(
            text='Тип:', font_size=sp(16), color=get_text_primary_color(), size_hint_y=None, height=dp(30)))
        self.content.add_widget(self.type_spinner)

        # date
        self._build_date_section()
        self._build_buttons()
        self.add_widget(self.content)
        Clock.schedule_once(lambda dt: Animation(opacity=1, d=0.3).start(self.content))

    def _build_date_section(self):
        date_section = BoxLayout(orientation='vertical', spacing=dp(10), size_hint_y=None, height=dp(200))
        with date_section.canvas.before:
            Color(rgba=(0.09, 0.50, 0.45, 1))
            self.date_rect = RoundedRectangle(pos=date_section.pos, size=date_section.size, radius=[dp(12)])
        date_section.bind(pos=self._update_date_rect, size=self._update_date_rect)

        self.start_spinners = self._create_date_row(self.start_date)
        date_section.add_widget(Label(text='З:', font_size=sp(16), color=get_text_primary_color(),
                                      size_hint_y=None, height=dp(30)))
        date_section.add_widget(self.start_spinners['row'])

        self.end_spinners = self._create_date_row(self.end_date)
        date_section.add_widget(Label(text='До:', font_size=sp(16), color=get_text_primary_color(),
                                      size_hint_y=None, height=dp(30)))
        date_section.add_widget(self.end_spinners['row'])

        self.content.add_widget(Label(size_hint_y=None, height=dp(10)))
        self.content.add_widget(date_section)

    def _create_date_row(self, date):
        days = [str(i).zfill(2) for i in range(1, 32)]
        months = [str(i).zfill(2) for i in range(1, 13)]
        years = [str(y) for y in range(datetime.now().year - 5, datetime.now().year + 1)]

        row = BoxLayout(orientation='horizontal', spacing=dp(5), size_hint_y=None, height=dp(45))
        day = CustomSpinner(text=str(date.day).zfill(2), values=days, size_hint=(0.3, 1), padding_x=dp(25))
        month = CustomSpinner(text=str(date.month).zfill(2), values=months, size_hint=(0.3, 1), padding_x=dp(25))
        year = CustomSpinner(text=str(date.year), values=years, size_hint=(0.4, 1), padding_x=dp(25))

        row.add_widget(day)
        row.add_widget(month)
        row.add_widget(year)

        return {'day': day, 'month': month, 'year': year, 'row': row}

    def _build_buttons(self):
        box = BoxLayout(size_hint_y=None, height=dp(45), spacing=dp(10))

        reset_btn = RoundedButton(text='[b]Скинути[/b]', bg_color='#445555', markup=True)
        close_btn = RoundedButton(text='[b]Закрити[/b]', bg_color='#666666', markup=True)
        apply_btn = RoundedButton(text='[b]Застосувати[/b]', bg_color='#0F7055', markup=True)

        reset_btn.bind(on_press=self._on_reset)
        close_btn.bind(on_press=lambda x: self.dismiss())
        apply_btn.bind(on_press=self._on_apply)

        box.add_widget(reset_btn)
        box.add_widget(close_btn)
        box.add_widget(apply_btn)

        self.content.add_widget(Label(size_hint_y=None, height=dp(10)))
        self.content.add_widget(box)

    def _on_reset(self, instance):
        now = datetime.now()
        last_year = datetime(now.year - 1, 1, 1)
        self.type_spinner.text = 'Витрати'

        for key in ['day', 'month', 'year']:
            self.start_spinners[key].text = getattr(last_year, key if key != 'day' else 'day').__str__().zfill(2)
            self.end_spinners[key].text = getattr(now, key if key != 'day' else 'day').__str__().zfill(2)

    def _on_apply(self, instance):
        try:
            start = self._parse_date(self.start_spinners)
            end = self._parse_date(self.end_spinners)
            self.current_type = self.type_spinner.text
            self.start_date = start
            self.end_date = end
            if hasattr(self, 'on_apply_callback'):
                self.on_apply_callback(self.current_type, start, end)
            self.dismiss()
        except Exception as e:
            print(f"Помилка фільтрації: {e}")

    def _parse_date(self, spinners):
        return datetime(
            int(spinners['year'].text), int(spinners['month'].text), int(spinners['day'].text)
        )

    def _update_rect(self, instance, value):
        if hasattr(self, 'bg_rect'):
            self.bg_rect.pos = instance.pos
            self.bg_rect.size = instance.size

    def _update_date_rect(self, instance, value):
        if hasattr(self, 'date_rect'):
            self.date_rect.pos = instance.pos
            self.date_rect.size = instance.size