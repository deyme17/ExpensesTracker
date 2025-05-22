from kivy.properties import ObjectProperty, StringProperty, ListProperty
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.lang import Builder

from datetime import datetime, timedelta

from app.views.screens.base_screen import BaseScreen
from app.views.widgets.transactions_widgets.transaction_row import TransactionRow
from app.views.widgets.transactions_widgets.add_transaction_popup import AddTransactionPopup
from app.views.widgets.transactions_widgets.filter_transaction_popup import FilterPopup
from app.views.widgets.transactions_widgets.sort_transaction_popup import SortPopup
from app.views.widgets.transactions_widgets.transaction_details_popup import TransactionDetailsPopup
from app.views.widgets.transactions_widgets.confirm_delete_popup import ConfirmDeletePopup
from app.views.widgets.transactions_widgets.account_select_popup import AccountSelectPopup
from app.services.local_storage import LocalStorageService
from app.utils.language_mapper import LanguageMapper as LM

Builder.load_file("kv/transactions_screen.kv")

class TransactionsScreen(BaseScreen):
    controller = ObjectProperty(None)
    balance_text = StringProperty("")
    account_options = ListProperty([])
    selected_account_id = StringProperty(allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.accounts = []
        self.transactions_data = {}
        self._initialized = False
        self.filter_start_date = datetime.now() - timedelta(days=365)
        self.filter_end_date = datetime.now()
        self._first_enter = True

        self._last_filter = {
            "min_amount": "0",
            "max_amount": "1000000",
            "start_date": self.filter_start_date,
            "end_date": self.filter_end_date,
            "type_selected": "all",
            "category_selected": "all",
            "payment_selected": "all"
        }
        self._last_sort = {
            "selected_field": "date",
            "ascending": True
        }

    def on_enter(self):
        if self._first_enter:
            self._first_enter = False

            self.storage_service = LocalStorageService()
            self.accounts = self.storage_service.get_accounts()
            acc_id = self.storage_service.get_active_account_id()
            if acc_id:
                self.selected_account_id = acc_id

            self.account_options = [f"{a.currency_code}-{a.type}" for a in self.accounts]
            self.update_balance_label()
            self.refresh_transactions()

    def update_balance_label(self):
        acc = next((a for a in self.accounts if a.account_id == self.selected_account_id), None)
        if acc:
            self.balance_text = f"{LM.field_name('balance')}: {acc.balance:.2f}"
        else:
            self.balance_text = f"{LM.field_name('balance')}: 0"

    def refresh_transactions(self):
        all_transactions = self.storage_service.get_transactions()
        filtered = [t for t in all_transactions if t.account_id == self.selected_account_id]
        self._clear_list()
        for tx in filtered:
            self._add_row(tx)

    def _clear_list(self):
        self.transactions_container.clear_widgets()
        self.transactions_data = {}

    def _add_row(self, tx):
        row = TransactionRow(
            transaction_id=tx.transaction_id,
            category=tx.category,
            amount=str(abs(tx.amount)),
            date=tx.get_formatted_date(),
            payment_method=tx.payment_method,
            type=tx.type,
            description=tx.description,
            currency=tx.currency,
            cashback=str(tx.cashback),
            commission=str(tx.commission),
            controller=self.controller,
            transactions_screen=self
        )
        self.transactions_container.add_widget(row)
        self.transactions_data[tx.transaction_id] = tx

    def add_transaction(self, type):
        popup = AddTransactionPopup(type=type, on_save=self._on_save)
        popup.open()

    def _on_save(self, type, category, amount, date, description, payment_method, currency, cashback, commission):
        success, msg = self.controller.add_transaction(
            type=type,
            category=category,
            amount=amount,
            date=date,
            description=description,
            payment_method=payment_method,
            currency=currency,
            cashback=cashback,
            commission=commission,
            account_id=self.selected_account_id
        )
        if success:
            Clock.schedule_once(self.refresh_transactions, 0.2)
            self.show_success_message(msg)
        else:
            self.show_error_message(msg)

    def edit_transaction(self, transaction_id):
        tx = self.transactions_data.get(transaction_id)
        if not tx:
            return
        popup = AddTransactionPopup(
            type=tx.type,
            existing_transaction=tx,
            on_save=self._on_update
        )
        popup.open()

    def _on_update(self, type, category, amount, date, description, payment_method, currency, cashback, commission, popup):
        tx_id = popup.transaction.transaction_id
        success, msg = self.controller.update_transaction(
            transaction_id=tx_id,
            type=type,
            category=category,
            amount=amount,
            date=date,
            description=description,
            payment_method=payment_method,
            currency=currency,
            cashback=cashback,
            commission=commission
        )
        if success:
            Clock.schedule_once(self.refresh_transactions, 0.2)
            self.show_success_message(msg)
        else:
            self.show_error_message(msg)

    def confirm_delete_transaction(self, transaction_id):
        popup = ConfirmDeletePopup(on_confirm=lambda: self._delete(transaction_id))
        popup.open()

    def _delete(self, transaction_id):
        result = self.controller.delete_transaction(transaction_id)
        if isinstance(result, tuple):
            deleted, msg = result
            if deleted:
                Clock.schedule_once(self.refresh_transactions, 0.2)
                self.show_success_message(msg)
            else:
                self.show_error_message(msg)
        else:
            self.show_error_message(message=LM.message("unable_delete_transaction"))

    def show_filter(self):
        popup = FilterPopup(on_apply=self._apply_filter, on_reset=self._reset_filter, **self._last_filter)
        popup.open()

    def _apply_filter(self, min_amount, max_amount, start_date, end_date, type, payment_method, category):
        self._last_filter.update({
            "min_amount": str(min_amount),
            "max_amount": str(max_amount),
            "start_date": start_date,
            "end_date": end_date,
            "type_selected": type or "all",
            "payment_selected": payment_method or "all",
            "category_selected": category or "all"
        })

        filtered = self.controller.filter_transactions(
            min_amount=min_amount,
            max_amount=max_amount,
            start_date=start_date,
            end_date=end_date,
            type=type,
            payment_method=payment_method,
            category=category
        )
        self._clear_list()
        for tx in filtered:
            self._add_row(tx)

        self.show_success_message(LM.message("filter_applied"))

    def _reset_filter(self):
        self._last_filter.update({
            "min_amount": "0",
            "max_amount": "1000000",
            "start_date": datetime.now() - timedelta(days=365),
            "end_date": datetime.now(),
            "type_selected": "all",
            "payment_selected": "all",
            "category_selected": "all"
        })

    def show_sort(self):
        popup = SortPopup(on_sort=self._apply_sort, **self._last_sort)
        popup.open()

    def _apply_sort(self, field_text, ascending):
        self._last_sort.update({
            "selected_field": field_text,
            "ascending": ascending
        })

        tx_list = list(self.transactions_data.values())
        sorted_list = self.controller.sort_transactions(tx_list, field=field_text, ascending=ascending)
        self._clear_list()
        for tx in sorted_list:
            self._add_row(tx)

        self.show_success_message(LM.message("sort_applied"))

    def show_transaction_details(self, transaction_id):
        tx = self.transactions_data.get(transaction_id)
        if not tx:
            self.show_error_message(LM.message("transaction_not_found"))
            return
        popup = TransactionDetailsPopup(
            transaction=tx,
            on_edit=lambda: self.edit_transaction(transaction_id),
            on_delete=lambda: self.confirm_delete_transaction(transaction_id)
        )
        popup.open()

    def open_account_selector(self):
        popup = AccountSelectPopup(
            self.accounts,
            on_account_selected=self._on_account_selected
        )
        popup.open()

    def _on_account_selected(self, selected_account_id):
        self.selected_account_id = selected_account_id
        self.storage_service.set_active_account(selected_account_id)
        self.update_balance_label()
        self.refresh_transactions()
        self.show_success_message(LM.message("account_changed"))