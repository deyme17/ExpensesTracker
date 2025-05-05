from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp, sp
from kivy.properties import DictProperty
from kivy.graphics import Color, RoundedRectangle
from kivy.utils import get_color_from_hex
from app.utils.theme import get_text_secondary_color, get_text_primary_color, STAT_COLORS

card_color = get_color_from_hex('#0A4035')

class StatsSection(GridLayout):
    """
    Widget for displaying statistical data in three columns and two rows,
    with a background card style.
    Shows fields: avg, min, max, total, count, top_category
    """
    stats_data = DictProperty({})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.cols = 3
        self.size_hint_y = None
        self.height = dp(150)
        self.padding = [dp(10), dp(10), dp(10), dp(10)]
        self.spacing = [dp(5), dp(10)]

        with self.canvas.before:
            Color(rgba=card_color)
            self._bg_rect = RoundedRectangle(pos=self.pos, size=self.size, radius=[dp(12)])
        self.bind(pos=self._update_bg, size=self._update_bg)

        fields = [
            ('Середнє',     'avg'),
            ('Мінімум',     'min'),
            ('Максимум',    'max'),
            ('Сума',        'total'),
            ('Кількість',   'count'),
            ('Топ категорія','top_category'),
        ]
        self._value_labels = {}
        for caption, key in fields:
            box = BoxLayout(orientation='vertical', padding=0, spacing=dp(2))
            lbl = Label(
                text=caption,
                font_size=sp(12),
                color=get_text_secondary_color(),
                size_hint_y=None,
                height=dp(20),
                halign='center',
                valign='middle'
            )
            lbl.bind(size=lbl.setter('text_size'))
            val = Label(
                text='—',
                font_size=sp(14),
                bold=True,
                color=get_text_primary_color(),
                halign='center',
                valign='middle'
            )
            val.bind(size=val.setter('text_size'))
            box.add_widget(lbl)
            box.add_widget(val)
            self._value_labels[key] = val
            self.add_widget(box)

    def _update_bg(self, *args):
        self._bg_rect.pos = self.pos
        self._bg_rect.size = self.size

    def update_stats(self, stats):
        """
        Refresh displayed statistics. Accepts either string or dict with value+color.
        """
        self.stats_data = stats
        for key, lbl in self._value_labels.items():
            value = stats.get(key, '—')
            if isinstance(value, dict):
                lbl.text = str(value.get('value', '—'))
                lbl.color = value.get('color', STAT_COLORS.get(key, get_text_primary_color()))
            else:
                lbl.text = str(value)
                lbl.color = STAT_COLORS.get(key, get_text_primary_color())

