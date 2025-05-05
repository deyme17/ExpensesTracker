from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.metrics import dp, sp
from kivy.properties import DictProperty
from app.utils.theme import get_text_primary_color

class StatsSection(BoxLayout):
    """
    Widget for displaying statistical data.
    Accepts dictionary values: avg, min, max, total, count, top_category
    """
    stats_data = DictProperty({})

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.orientation = 'vertical'
        self.spacing = dp(8)
        self.padding = dp(10)
        self._labels = {}
        self._build_layout()

    def _build_layout(self):
        fields = [
            ('Середнє значення:', 'avg'),
            ('Мінімальне значення:', 'min'),
            ('Максимальне значення:', 'max'),
            ('Загальна сума:', 'total'),
            ('Кількість транзакцій:', 'count'),
            ('Найчастіша категорія:', 'top_category'),
        ]
        for label_text, key in fields:
            row = BoxLayout(orientation='horizontal', size_hint_y=None, height=dp(30))
            label = Label(
                text=label_text,
                font_size=sp(14),
                color=get_text_primary_color(),
                size_hint_x=0.6,
                halign='left', valign='middle'
            )
            label.bind(size=label.setter('text_size'))

            value_label = Label(
                text=self.stats_data.get(key, '—'),
                font_size=sp(14),
                color=get_text_primary_color(),
                size_hint_x=0.4,
                halign='right', valign='middle'
            )
            value_label.bind(size=value_label.setter('text_size'))
            self._labels[key] = value_label
            row.add_widget(label)
            row.add_widget(value_label)
            self.add_widget(row)

    def update_stats(self, stats):
        """
        Refresh the statistics display.
        """
        self.stats_data = stats
        for key, label in self._labels.items():
            label.text = self.stats_data.get(key, '—')
