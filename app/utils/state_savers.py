from app.utils.constants import ALL, DATE_FIELD, EXPENSE
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

class AnalyticsFilterState:
    def __init__(self, current_type=EXPENSE, start_date=None, end_date=None):
        now = datetime.now()
        self.current_type = current_type
        self.start_date = start_date or datetime(now.year - 1, 1, 1)
        self.end_date = end_date or now

    def to_dict(self):
        return {
            "current_type": self.current_type,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }

    def update(self, *, current_type=None, start_date=None, end_date=None):
        if current_type is not None:
            self.current_type = current_type
        if start_date is not None:
            self.start_date = start_date
        if end_date is not None:
            self.end_date = end_date

    def reset(self):
        now = datetime.now()
        self.current_type = EXPENSE
        self.start_date = datetime(now.year - 1, 1, 1)
        self.end_date = now

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