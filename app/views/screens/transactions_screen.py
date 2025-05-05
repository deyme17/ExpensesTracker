from kivy.properties import ObjectProperty
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.lang import Builder

from kivy.uix.boxlayout import BoxLayout

from app.views.screens.base_screen import BaseScreen
from app.views.widgets.transactions_widgets.transaction_row import TransactionRow
from app.views.widgets.buttons.floating_button import FloatingActionButton
from app.views.widgets.transactions_widgets.add_transaction_popup import AddTransactionPopup
from app.views.widgets.transactions_widgets.filter_transaction_popup import FilterPopup
from app.views.widgets.transactions_widgets.sort_transaction_popup import SortPopup
from app.views.widgets.transactions_widgets.transaction_details_popup import TransactionDetailsPopup
from app.views.widgets.transactions_widgets.confirm_delete_popup import ConfirmDeletePopup
from app.views.widgets.popups.alert_popup import ErrorPopup, SuccessPopup
from app.views.widgets.popups.menu_popup import MenuPopup
from app.utils.theme import get_accent_color

Builder.load_file('kv/transactions_screen.kv')

class TransactionsScreen(BaseScreen):
    controller = ObjectProperty(None)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.transactions_data = {}
        self._initialized = False

    def on_enter(self):
        super().on_enter()
        if not self._initialized:
            self.refresh_transactions()
            self._initialized = True

    def _clear_list(self):
        self.transactions_container.clear_widgets()
        self.transactions_data = {}

    def _add_row(self, tx):
        row = TransactionRow(
            transaction_id=tx.transaction_id,
            category=tx.category,
            amount=str(abs(tx.amount)),
            date=tx.get_formatted_date(),
            is_income=tx.is_income,
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

    def refresh_transactions(self, *args):
        if not self.controller:
            return
        transactions = self.controller.get_transactions(force_refresh=True)
        self._clear_list()
        for tx in transactions:
            self._add_row(tx)

    def add_transaction(self, is_income=True):
        popup = AddTransactionPopup(is_income=is_income, on_save=self._on_save)
        popup.open()

    def edit_transaction(self, transaction_id):
        tx = self.transactions_data.get(transaction_id)
        if not tx:
            return
        popup = AddTransactionPopup(
            is_income=tx.is_income,
            existing_transaction=tx,
            on_save=self._on_update
        )
        popup.open()

    def _on_save(self, is_income, category, amount, date, description, payment_method, currency, cashback, commission):
        success, msg = self.controller.add_transaction(
            is_income=is_income,
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
            SuccessPopup(message=msg).open()
            Clock.schedule_once(self.refresh_transactions, 0.2)
        else:
            ErrorPopup(message=msg).open()

    def _on_update(self, is_income, category, amount, date, description, payment_method, currency, cashback, commission, popup):
        tx_id = popup.transaction.transaction_id
        success, msg = self.controller.update_transaction(
            transaction_id=tx_id,
            is_income=is_income,
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
            ErrorPopup(message="Unable to delete transaction").open()

    def show_filter(self):
        popup = FilterPopup(on_apply=self._apply_filter)
        popup.open()

    def _apply_filter(self, min_amount, max_amount, start_date, end_date, is_income, payment_method):
        filtered = self.controller.filter_transactions(
            min_amount=min_amount,
            max_amount=max_amount,
            start_date=start_date,
            end_date=end_date,
            is_income=is_income,
            payment_method=payment_method
        )
        self._clear_list()
        for tx in filtered:
            self._add_row(tx)

    def show_sort(self):
        popup = SortPopup(on_sort=self._apply_sort)
        popup.open()

    def _apply_sort(self, field_text, ascending):
        field_map = {'Дата': 'date', 'Сума': 'amount', 'Кешбек': 'cashback', 'Комісія': 'commission'}
        key = field_map.get(field_text, 'date')
        tx_list = list(self.transactions_data.values())
        sorted_list = self.controller.sort_transactions(tx_list, field=key, ascending=ascending)
        self._clear_list()
        for tx in sorted_list:
            self._add_row(tx)

    def show_transaction_details(self, transaction_id):
        tx = self.transactions_data.get(transaction_id)
        if not tx:
            ErrorPopup(message="Transaction not found").open()
            return
        popup = TransactionDetailsPopup(
            transaction=tx,
            on_edit=lambda: self.edit_transaction(transaction_id),
            on_delete=lambda: self.confirm_delete_transaction(transaction_id)
        )
        popup.open()

    def show_menu(self, *args):
        popup = MenuPopup(on_logout=self._logout, on_exit=self._exit_app)
        popup.open()

    def go_analytics(self):
        if self.manager:
            self.manager.transition.direction = 'left'
            self.manager.current = 'analytics_screen'

    def _logout(self):
        from kivy.app import App
        app = App.get_running_app()
        if hasattr(app, 'auth_controller'):
            app.auth_controller.logout()
        self.switch_screen('first_screen', 'right')

    def _exit_app(self):
        from kivy.core.window import Window
        Window.close()

    def show_success_message(self, message):
        SuccessPopup(message=message).open()

    def show_error_message(self, message):
        ErrorPopup(message=message).open()
