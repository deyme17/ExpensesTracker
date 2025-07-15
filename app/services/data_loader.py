from typing import Callable, Optional
from kivy.clock import Clock
import threading


class DataLoader:
    """
    Handles asynchronous loading of financial data.
    Args:
        storage_service: Storage handler for persistent data
        account_service: Account operations service
        transaction_service: Transaction operations service
        category_service: Category operations service
        currency_service: Currency operations service
    """
    def __init__(
        self,
        storage_service,
        account_service,
        transaction_service,
        category_service,
        currency_service
    ):
        self.storage = storage_service
        self.account_service = account_service
        self.transaction_service = transaction_service
        self.category_service = category_service
        self.currency_service = currency_service

    def load_data(self, user, callback: Optional[Callable[[], None]] = None) -> None:
        """
        Loads all financial data asynchronously.
        Args:
            user: Authenticated user
            callback: Optional function to execute after loading completes (on main thread)
        """
        def _execute_load():
            try:
                self.account_service.user_id = user.user_id
                self.transaction_service.user_id = user.user_id
                self.transaction_service.storage = self.storage

                accounts, _ = self.account_service.get_accounts()
                self.transaction_service.get_transactions(force_refresh=True)
                self.category_service.get_categories()
                self.currency_service.get_currencies()

                if accounts:
                    previous_account_id = self.storage.settings.get(user.user_id, "active_account_id")
                    matching_account = next((acc for acc in accounts if acc.account_id == previous_account_id), None)

                if matching_account:
                    self.storage.settings.set(user.user_id, "active_account_id", previous_account_id)
                elif accounts:
                    self.storage.settings.set(user.user_id, "active_account_id", accounts[0].account_id)

            except Exception as e:
                print(f"[DataLoader] Error: {e}")

            finally:
                if callback:
                    Clock.schedule_once(lambda dt: callback())

        threading.Thread(target=_execute_load, daemon=True).start()