from app.utils.constants import ALL, DATE_FIELD
from datetime import datetime, timedelta

class FilterState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.min_amount = "0"
        self.max_amount = "1000000"
        self.start_date = datetime.now() - timedelta(days=365)
        self.end_date = datetime.now()
        self.type_selected = ALL
        self.category_selected = ALL
        self.payment_selected = ALL

    def to_dict(self):
        return {
            "min_amount": self.min_amount,
            "max_amount": self.max_amount,
            "start_date": self.start_date,
            "end_date": self.end_date,
            "type_selected": self.type_selected,
            "category_selected": self.category_selected,
            "payment_selected": self.payment_selected,
        }

class SortState:
    def __init__(self):
        self.selected_field = DATE_FIELD
        self.ascending = True

    def update(self, selected_field, ascending):
        self.selected_field = selected_field
        self.ascending = ascending

    def to_dict(self):
        return {
            "selected_field": self.selected_field,
            "ascending": self.ascending
        }