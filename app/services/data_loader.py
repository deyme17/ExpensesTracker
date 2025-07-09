from kivy.clock import Clock


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
    def __init__(self,
                 storage_service,
                 account_service,
                 transaction_service,
                 category_service,
                 currency_service):
        self.storage = storage_service
        self.account_service = account_service
        self.transaction_service = transaction_service
        self.category_service = category_service
        self.currency_service = currency_service

    def load_data(self, user, callback=None):
        """
        Loads all financial data asynchronously.
        Args:
            user:
            callback: Optional function to execute after loading completes
        """
        def _execute_load(dt):
            try:
                self.account_service.user_id = user.user_id
                self.transaction_service.user_id = user.user_id
                self.transaction_service.storage = self.storage

                accounts, _ = self.account_service.get_accounts()

                self.transaction_service.get_transactions(force_refresh=True)
                self.category_service.get_categories()
                self.currency_service.get_currencies()

                if accounts:
                    previous_account_id = self.storage.get_active_account_id()
                    matching_account = next((acc for acc in accounts if acc.account_id == previous_account_id), None)

                    if matching_account:
                        self.storage.set_active_account(previous_account_id)
                    else:
                        self.storage.set_active_account(accounts[0].account_id)

            except Exception as e:
                print(f"[DataLoader] Error: {e}")
            finally:
                if callback:
                    callback()

        Clock.schedule_once(_execute_load)
