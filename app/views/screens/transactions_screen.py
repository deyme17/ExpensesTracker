from kivy.properties import StringProperty, ListProperty
from kivy.clock import Clock
from kivy.lang import Builder

from app.views.screens.base_screen import BaseScreen
from app.views.widgets.transactions_widgets import (TransactionRow, AddTransactionPopup, 
                                                    FilterPopup, SortPopup, TransactionDetailsPopup, 
                                                    ConfirmDeletePopup, AccountSelectPopup)

from app.utils.language_mapper import LanguageMapper as LM
from app.utils.formatters import format_date
from app.utils.state_savers import FilterState, SortState


Builder.load_file("kv/transactions_screen.kv")


class TransactionsScreen(BaseScreen):
    """
    Screen for displaying and managing financial transactions.
    Args:
        transactions_controller: Handles transaction operations
        meta_data_controller: Provides currency/category metadata
        local_storage: Persistent local_storage handler
        update_analytics_callback: Callback for analytics updates
    """
    balance_text = StringProperty("")
    account_options = ListProperty([])
    selected_account_id = StringProperty(allownone=True)

    def __init__(self, transactions_controller, meta_data_controller, local_storage, update_analytics_callback=None, **kwargs):
        super().__init__(**kwargs)
        # controllers
        self.transactions_controller = transactions_controller
        self.meta_data_controller = meta_data_controller
        self.local_storage = local_storage
        # callback
        self.update_analytics_callback = update_analytics_callback
        # data
        self._first_enter = True
        self.accounts = []
        self.transactions_data = {}
        self.categories = []
        self.currencies = []
        # cash
        self._filter_state = FilterState()
        self._sort_state = SortState()

    @property
    def selected_account(self):
        return next((a for a in self.accounts if a.account_id == self.selected_account_id), None)
    
    @property
    def current_user_id(self):
        try:
            return self.local_storage.settings.get_current_user_id()
        except Exception as e:
            print(f"[ERROR] Failed to get current user ID: {e}")
            return None
        
    def on_enter(self):
        if self._first_enter:
            self._first_enter = False
            self._initialize_data()

# transaction popup
    def _open_transaction_popup(self, *, type: str, existing_transaction = None):
        popup = AddTransactionPopup(
            currencies=self.currencies,
            categories=self.categories,
            type=type,
            existing_transaction=existing_transaction,
            on_save=self._save_or_update_transaction
        )
        popup.open()

    def add_transaction(self, type: str):
        self._open_transaction_popup(type=type)

    def edit_transaction(self, transaction_id: str):
        tx = self.transactions_data.get(transaction_id)
        if tx:
            self._open_transaction_popup(type=tx.type, existing_transaction=tx)

    def _save_or_update_transaction(self, transaction_data: dict, transaction_id: str =None):
        success, msg = self.transactions_controller.update_transaction(
            transaction_id=transaction_id,
            account_id=self.selected_account_id,
            **transaction_data
        )
        if success:
            Clock.schedule_once(lambda dt: self.refresh_transactions(), 0.2)
            self.trigger_analytics_update()
            self.show_success_message(LM.message("transaction_updated" if transaction_id else "transaction_saved"))
            return True
        else:
            self.show_error_message(msg)
            return False

# transaction deleting
    def confirm_delete_transaction(self, transaction_id: str):
        popup = ConfirmDeletePopup(on_confirm=lambda: self._delete(transaction_id))
        popup.open()

    def _delete(self, transaction_id: str):
        result = self.transactions_controller.delete_transaction(transaction_id)
        deleted, msg = result if isinstance(result, tuple) else (False, None)
        if deleted:
            Clock.schedule_once(lambda dt: self.refresh_transactions(), 0)
            self.trigger_analytics_update()
            Clock.schedule_once(lambda dt: self.show_success_message(LM.message("transaction_deleted")), 3)
        else:
            print("[DEBUG] Delete failed:", msg)
            self.show_error_message(LM.message("unable_delete_transaction"))

# filter
    def show_filter(self):
        popup = FilterPopup(
            filter_state=self._filter_state,
            categories=self.categories,
            on_apply=self._apply_filter,
            on_reset=self._reset_filter
        )
        popup.open()

    def _apply_filter(self, min_amount, max_amount, start_date, end_date, type, payment_method, category):
        filtered = self.transactions_controller.filter_transactions(
            min_amount=min_amount,
            max_amount=max_amount,
            start_date=start_date,
            end_date=end_date,
            type=type,
            payment_method=payment_method,
            category=category,
            account_id=self.selected_account_id
        )
        self._display_transactions(filtered)
        self.show_success_message(LM.message("filter_applied"))

    def _reset_filter(self):
        self._filter_state.reset()

# sort
    def show_sort(self):
        popup = SortPopup(on_sort=self._apply_sort, **self._sort_state.to_dict())
        popup.open()

    def _apply_sort(self, field_text: str, ascending: bool):
        self._sort_state.update(
            selected_field=field_text,
            ascending=ascending
        )
        tx_list = list(self.transactions_data.values())
        sorted_tx = self.transactions_controller.sort_transactions(tx_list, field=field_text, ascending=ascending)
        self._display_transactions(sorted_tx)
        self.show_success_message(LM.message("sort_applied"))

# transaction datails
    def show_transaction_details(self, transaction_id: str):
        tx = self.transactions_data.get(transaction_id)
        if not tx:
            self.show_error_message(LM.message("transaction_not_found"))
            return
        popup = TransactionDetailsPopup(
            transaction=tx,
            meta_data_controller=self.meta_data_controller,
            on_edit=lambda: self.edit_transaction(transaction_id),
            on_delete=lambda: self.confirm_delete_transaction(transaction_id)
        )
        popup.open()

# account selection
    def open_account_selector(self):
        popup = AccountSelectPopup(
            self.accounts,
            on_account_selected=self._on_account_selected
        )
        popup.open()

    def _on_account_selected(self, selected_account_id: str):
        try:
            self.selected_account_id = selected_account_id
            print(f"[DEBUG] Account selected: {selected_account_id}")
            user_id = self.current_user_id
            if user_id:
                self.local_storage.settings.set_active_account_id(user_id, selected_account_id)
            self._refresh_everything()
            self.show_success_message(LM.message("account_changed"))
        except Exception as e:
            print(f"[ERROR] Failed to select account: {e}")
            self.show_error_message(LM.message("failed_to_select_account"))

# other
    def refresh_transactions(self, force: bool =False):
        all_tx, _ = self.transactions_controller.get_transactions(force_refresh=force)
        filtered = [tx for tx in all_tx if tx.account_id == self.selected_account_id]
        filtered = sorted(filtered, key=lambda t: t.date, reverse=True)
        self._display_transactions(filtered)

    def update_balance_label(self):
        acc = self.selected_account
        if acc:
            self.balance_text = f"{LM.field_name('balance')}: {acc.balance:.2f}"
        else:
            self.balance_text = f"{LM.field_name('balance')}: 0"

    def trigger_analytics_update(self):
        if self.update_analytics_callback:
            self.update_analytics_callback()

    def _refresh_everything(self):
        self.refresh_transactions()
        self.update_balance_label()
        self.trigger_analytics_update()

    def _initialize_data(self):
        try:
            user_id = self.current_user_id
            if not user_id:
                self.show_error_message(LM.message("no_user_logged_in"))
                return
            # account
            self.accounts = self.local_storage.accounts.get_accounts_by_id(user_id) or []
            self.selected_account_id = self.local_storage.settings.get_active_account_id(user_id)
            
            if not self.selected_account_id and self.accounts:
                self.selected_account_id = self.accounts[0].account_id
                self.local_storage.settings.set_active_account_id(user_id, self.selected_account_id)

            self.account_options = [f"{a.currency_code}-{a.type}" for a in self.accounts]
            
            # metadata
            self.categories = self.meta_data_controller.get_categories()
            self.currencies = self.meta_data_controller.get_currencies()
            
            # refresh everything
            self._refresh_everything()
            
        except Exception as e:
            print(f"[ERROR] Failed to initialize data: {e}")
            self.show_error_message(LM.message("failed_to_initialize_screen"))

    def _display_transactions(self, transactions: list):
        self._clear_list()
        for tx in transactions:
            self._add_row(tx)

    def _clear_list(self):
        self.transactions_container.clear_widgets()
        self.transactions_data = {}

    def _add_row(self, tx):
        category_name = self.meta_data_controller.get_category_name_by_mcc(tx.mcc_code)
        currency_name = self.meta_data_controller.get_currency_name_by_code(tx.currency_code)
        
        row = TransactionRow(
            transaction_id=tx.transaction_id,
            category=category_name,
            amount=str(abs(tx.amount)),
            date=format_date(tx.date),
            payment_method=tx.payment_method,
            type=tx.type,
            description=tx.description,
            currency=currency_name,
            cashback=str(tx.cashback),
            commission=str(tx.commission),
            controller=self.transactions_controller,
            transactions_screen=self
        )
        self.transactions_container.add_widget(row)
        self.transactions_data[tx.transaction_id] = tx
        
    def go_analytics(self):
        if self.manager:
            self.manager.transition.direction = 'left'
            self.manager.current = 'analytics_screen'