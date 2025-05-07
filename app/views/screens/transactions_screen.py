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
from app.views.widgets.popups.alert_popup import ErrorPopup, SuccessPopup
from app.views.widgets.popups.menu_popup import MenuPopup
from app.views.widgets.transactions_widgets.account_select_popup import AccountSelectPopup
from app.services.local_storage import LocalStorageService
from app.utils.constants import UNABLE_DEL_TR, TR_NOT_FOUND, TR_TYPE_MAP_UA_ENG, PYMNT_METHOD_MAP_UA_ENG, FIELD_MAP

Builder.load_file("kv/transactions_screen.kv")

class TransactionsScreen(BaseScreen):
    controller = ObjectProperty(None)
    balance_text = StringProperty("Баланс: 0")
    account_options = ListProperty([])
    selected_account_id = StringProperty(allownone=True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.accounts = []
        self.transactions_data = {}
        self._initialized = False
        self.filter_start_date = datetime.now() - timedelta(days=365)
        self.filter_end_date = datetime.now()

    def on_enter(self):
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
            self.balance_text = f"Баланс ({acc.currency_code}-{acc.type}): {acc.balance:.2f}"
        else:
            self.balance_text = "Баланс: 0"

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
            is_income=(tx.type == "income"),
            payment_method=tx.payment_method,
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
        internal_type = TR_TYPE_MAP_UA_ENG.get(type, type)
        internal_method = PYMNT_METHOD_MAP_UA_ENG.get(payment_method, payment_method)
        success, msg = self.controller.add_transaction(
            type=internal_type,
            category=category,
            amount=amount,
            date=date,
            description=description,
            payment_method=internal_method,
            currency=currency,
            cashback=cashback,
            commission=commission,
            account_id=self.selected_account_id
        )
        if success:
            SuccessPopup(message=msg).open()
            Clock.schedule_once(self.refresh_transactions, 0.2)
        else:
            ErrorPopup(message=msg).open()

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
        internal_type = TR_TYPE_MAP_UA_ENG.get(type, type)
        internal_method = PYMNT_METHOD_MAP_UA_ENG.get(payment_method, payment_method)
        success, msg = self.controller.update_transaction(
            transaction_id=tx_id,
            type=internal_type,
            category=category,
            amount=amount,
            date=date,
            description=description,
            payment_method=internal_method,
            currency=currency,
            cashback=cashback,
            commission=commission
        )
        if success:
            SuccessPopup(message=msg).open()
            Clock.schedule_once(self.refresh_transactions, 0.2)
        else:
            ErrorPopup(message=msg).open()

    def confirm_delete_transaction(self, transaction_id):
        popup = ConfirmDeletePopup(on_confirm=lambda: self._delete(transaction_id))
        popup.open()

    def _delete(self, transaction_id):
        result = self.controller.delete_transaction(transaction_id)
        if isinstance(result, tuple):
            deleted, msg = result
            if deleted:
                SuccessPopup(message=msg).open()
                Clock.schedule_once(self.refresh_transactions, 0.2)
            else:
                ErrorPopup(message=msg).open()
        else:
            ErrorPopup(message=UNABLE_DEL_TR).open()

    def show_filter(self):
        popup = FilterPopup(on_apply=self._apply_filter)
        popup.open()

    def _apply_filter(self, min_amount, max_amount, start_date, end_date, type, payment_method, category):
        internal_type = TR_TYPE_MAP_UA_ENG.get(type, type)
        internal_method = PYMNT_METHOD_MAP_UA_ENG.get(payment_method, payment_method)
        filtered = self.controller.filter_transactions(
            min_amount=min_amount,
            max_amount=max_amount,
            start_date=start_date,
            end_date=end_date,
            type=internal_type,
            payment_method=internal_method,
            category=category
        )
        self._clear_list()
        for tx in filtered:
            self._add_row(tx)

        self.show_success_message("Фільтр застосовано")

    def show_sort(self):
        popup = SortPopup(on_sort=self._apply_sort)
        popup.open()

    def _apply_sort(self, field_text, ascending):
        key = FIELD_MAP.get(field_text, "date")
        tx_list = list(self.transactions_data.values())
        sorted_list = self.controller.sort_transactions(tx_list, field=key, ascending=ascending)
        self._clear_list()
        for tx in sorted_list:
            self._add_row(tx)

        self.show_success_message("Сортування застосовано")

    def show_transaction_details(self, transaction_id):
        tx = self.transactions_data.get(transaction_id)
        if not tx:
            ErrorPopup(message=TR_NOT_FOUND).open()
            return
        popup = TransactionDetailsPopup(
            transaction=tx,
            on_edit=lambda: self.edit_transaction(transaction_id),
            on_delete=lambda: self.confirm_delete_transaction(transaction_id)
        )
        popup.open()

    def go_analytics(self):
        if self.manager:
            self.manager.transition.direction = "left"
            self.manager.current = "analytics_screen"