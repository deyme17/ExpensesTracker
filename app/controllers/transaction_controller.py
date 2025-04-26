from app.models.transaction import Transaction
from app.models.category import Category
from datetime import datetime
import random


class TransactionController:    
    def __init__(self, storage_service, monobank_service):
        """
        Init the transaction controller.
        
        Args:
            storage_service: Service for storing transaction data
            monobank_service: Service for interacting with Monobank API
        """
        self.storage_service = storage_service
        self.monobank_service = monobank_service
        
        self.init_categories()    # TODO
    
    def init_categories(self):
        """Initialize transaction categories."""
        self.income_categories = [
            Category(name='Зарплата', is_income=True),
            Category(name='Подарунок', is_income=True),
            Category(name='Дивіденди', is_income=True),
            Category(name='Фріланс', is_income=True),
            Category(name='Відсотки', is_income=True),
            Category(name='Інше', is_income=True)
        ]
        
        self.expense_categories = [
            Category(name='Продукти', is_income=False),
            Category(name='Транспорт', is_income=False),
            Category(name='Розваги', is_income=False),
            Category(name='Здоров\'я', is_income=False),
            Category(name='Одяг', is_income=False),
            Category(name='Кафе', is_income=False),
            Category(name='Зв\'язок', is_income=False),
            Category(name='Інше', is_income=False)
        ]
        
        self.storage_service.save_categories(self.income_categories + self.expense_categories)
    
    def get_transactions(self, force_refresh=False):
        """
        Get all transactions for the current user.
        
        Args:
            force_refresh: If True, fetch new transactions from Monobank
                          instead of using cached data
        
        Returns:
            List of Transaction objects
        """
        # try to get from storage first
        transactions = self.storage_service.get_transactions()
        
        # if no transaction/forve_refresh, try to fetch from Monobank
        if not transactions or force_refresh:
            user = self.storage_service.get_user()
            if user and user.token:
                try:
                    # fetching
                    monobank_transactions = self.monobank_service.get_transactions(user.token)
                    if monobank_transactions:
                        # convert&save
                        transactions = self._convert_monobank_transactions(monobank_transactions)
                        self.storage_service.save_transactions(transactions)
                except Exception as e:
                    print(f"Error fetching transactions from Monobank: {e}")

        # TODO del it
        if not transactions:
            transactions = self._generate_sample_transactions()
            self.storage_service.save_transactions(transactions)
        
        return transactions
    
    def add_transaction(self, category, amount, date, description, is_income, 
                        payment_method, currency='UAH', cashback='0', commission='0'):
        """
        Add a new transaction.
        
        Args:
            category: Transaction category name
            amount: Transaction amount
            date: Transaction date string (DD.MM.YYYY)
            description: Transaction description
            is_income: Whether this is an income transaction
            payment_method: Payment method ('Картка' or 'Готівка')
            currency: Currency code
            cashback: Cashback amount
            commission: Commission amount
            
        Returns:
            Transaction: The created transaction
        """
        try:
            # parsing
            amount = float(amount.replace(',', '.'))
            if amount <= 0:
                return None, "Сума має бути позитивним числом"
            
            # parse date
            day, month, year = date.split('.')
            transaction_date = datetime(int(year), int(month), int(day))
            
            # parse cashback and commission
            cashback = float(cashback.replace(',', '.'))
            commission = float(commission.replace(',', '.'))
            
            # create transaction
            transaction = Transaction(
                transaction_id=f"tr_{random.randint(10000, 99999)}", # TODO ??
                user_id=self.storage_service.get_user().user_id,
                amount=amount if is_income else -amount,
                date=transaction_date,
                category=category,
                description=description,
                is_income=is_income,
                payment_method=payment_method,
                currency=currency,
                cashback=cashback,
                commission=commission
            )
            
            # save transaction
            self.storage_service.add_transaction(transaction)
            
            return transaction, "Транзакцію додано"
        
        except ValueError:
            return None, "Некоректне значення суми. Введіть числове значення."
        except Exception as e:
            return None, f"Помилка: {str(e)}"
    
    def update_transaction(self, transaction_id, category, amount, date, description, 
                           is_income, payment_method, currency='UAH', cashback='0', commission='0'):
        """
        Update an existing transaction.
        
        Args:
            transaction_id: ID of the transaction to update
            [other parameters same as add_transaction]
            
        Returns:
            Transaction: The updated transaction
        """
        try:
            # get transaction
            original_transaction = self.storage_service.get_transaction(transaction_id)
            if not original_transaction:
                return None, "Не вдалося знайти транзакцію для оновлення"
            
            # parse amount
            amount = float(amount.replace(',', '.'))
            if amount <= 0:
                return None, "Сума має бути позитивним числом"
            
            # parse date
            day, month, year = date.split('.')
            transaction_date = datetime(int(year), int(month), int(day))
            
            # parse cashback and commission
            cashback = float(cashback.replace(',', '.'))
            commission = float(commission.replace(',', '.'))
            
            # update transaction
            transaction = Transaction(
                transaction_id=transaction_id,
                user_id=original_transaction.user_id,
                amount=amount if is_income else -amount,
                date=transaction_date,
                category=category,
                description=description,
                is_income=is_income,
                payment_method=payment_method,
                currency=currency,
                cashback=cashback,
                commission=commission
            )
            
            # save transaction
            self.storage_service.update_transaction(transaction)
            
            return transaction, "Транзакцію оновлено"
        
        except ValueError:
            return None, "Некоректне значення суми. Введіть числове значення."
        except Exception as e:
            return None, f"Помилка: {str(e)}"
    
    def delete_transaction(self, transaction_id):
        """
        Delete a transaction.
        
        Args:
            transaction_id: ID of the transaction to delete
            
        Returns:
            tuple: (success, message)
        """
        try:
            transaction = self.storage_service.get_transaction(transaction_id)
            if not transaction:
                return False, "Транзакцію не знайдено"
            
            # delete transaction
            self.storage_service.delete_transaction(transaction_id)
            return True, "Транзакцію видалено"
        except Exception as e:
            return False, f"Помилка: {str(e)}"
    
    def filter_transactions(self, min_amount=None, max_amount=None, 
                           start_date=None, end_date=None, 
                           transaction_type=None, payment_method=None):
        """
        Filter transactions based on criteria.
        
        Args:
            min_amount: Minimum transaction amount
            max_amount: Maximum transaction amount
            start_date: Start date for filtering (datetime)
            end_date: End date for filtering (datetime)
            transaction_type: 'Доходи', 'Витрати', or None (all)
            payment_method: 'Картка', 'Готівка', or None (all)
            
        Returns:
            List of filtered Transaction objects
        """
        transactions = self.get_transactions()
        filtered = []
        
        # string to float
        if min_amount is not None and isinstance(min_amount, str):
            try:
                min_amount = float(min_amount.replace(',', '.'))
            except ValueError:
                min_amount = 0
        
        if max_amount is not None and isinstance(max_amount, str):
            try:
                max_amount = float(max_amount.replace(',', '.'))
            except ValueError:
                max_amount = float('inf')
        
        # apply filters
        for transaction in transactions:
            amount = abs(transaction.amount)
            
            # filter by amount
            if min_amount is not None and amount < min_amount:
                continue
            if max_amount is not None and amount > max_amount:
                continue
            
            # filter by date
            if start_date is not None and transaction.date < start_date:
                continue
            if end_date is not None and transaction.date > end_date:
                continue
            
            # filter by type
            if transaction_type == 'Доходи' and not transaction.is_income:
                continue
            if transaction_type == 'Витрати' and transaction.is_income:
                continue
            
            # filter by payment method
            if payment_method is not None and payment_method != 'Всі':
                if transaction.payment_method != payment_method:
                    continue
            
            filtered.append(transaction)
        
        return filtered
    
    def sort_transactions(self, field, ascending=True):
        """
        Sort transactions by the specified field.
        
        Args:
            field: Field to sort by ('Дата', 'Сума', 'Категорія', etc.)
            ascending: Sort order (True for ascending, False for descending)
            
        Returns:
            List of sorted Transaction objects
        """
        transactions = self.get_transactions()
        
        def sort_key(transaction):
            if field == 'Дата':
                return transaction.date
            elif field == 'Сума':
                return abs(transaction.amount)
            elif field == 'Категорія':
                return transaction.category
            elif field == 'Тип оплати':
                return transaction.payment_method
            elif field == 'Кешбек':
                return transaction.cashback
            elif field == 'Комісія':
                return transaction.commission
            return 0
        
        return sorted(transactions, key=sort_key, reverse=not ascending)
    
    def get_categories(self, is_income=None):
        """
        Get transaction categories.
        
        Args:
            is_income: If True, get income categories; if False, get expense categories;
                      if None, get all categories
        
        Returns:
            List of Category objects
        """
        if is_income is None:
            return self.income_categories + self.expense_categories
        elif is_income:
            return self.income_categories
        else:
            return self.expense_categories
    
    def _convert_monobank_transactions(self, monobank_transactions):
        """
        Convert Monobank transactions to our Transaction model.
        
        Args:
            monobank_transactions: List of transactions from Monobank API
            
        Returns:
            List of Transaction objects
        """
        user = self.storage_service.get_user()
        transactions = []
        
        for mt in monobank_transactions:
            # Map Monobank category to our category
            category = self._map_monobank_category(mt.get('mcc'), mt.get('amount', 0) > 0)
            
            transaction = Transaction(
                transaction_id=f"mb_{mt.get('id')}",  # TODO
                user_id=user.user_id,
                amount=mt.get('amount') / 100.0,
                date=datetime.fromtimestamp(mt.get('time')),
                category=category.name,
                description=mt.get('description', ''),
                is_income=mt.get('amount', 0) > 0,
                payment_method='Картка',
                currency=mt.get('currencyCode', 980),  # UAH
                cashback=mt.get('cashbackAmount', 0) / 100.0,
                commission=0.0
            )
            
            transactions.append(transaction)
        
        return transactions
    
    def _map_monobank_category(self, mcc, is_income): # TODO
        """Map Monobank MCC code to our categories."""
        if is_income:
            return self.income_categories[0]  # default to first income category
        else:
            mcc_mapping = {
                5411: 'Продукти',   
                4111: 'Транспорт',  
                7832: 'Розваги',    
                8011: 'Здоров\'я',   
                5651: 'Одяг',      
                5814: 'Кафе',       
                4814: 'Зв\'язок'     
            }
            
            category_name = mcc_mapping.get(mcc, 'Інше')
            for category in self.expense_categories:
                if category.name == category_name:
                    return category
            
            return self.expense_categories[-1]

    def show_transaction_details(self, transaction_id):
        """
        Method to retrieve transaction details and pass them to the appropriate screen.

        Args:
            transaction_id: The transaction ID to view
        """
        transaction = self.storage_service.get_transaction(transaction_id)
        
        if not transaction:
            print(f"Помилка: Транзакцію з ID {transaction_id} не знайдено")
            return None
        
        return transaction
    
    def _generate_sample_transactions(self):    # TODO DEL 
        """Generate sample transactions for testing."""
        from datetime import timedelta
        
        user = self.storage_service.get_user()
        if not user:
            return []
        
        transactions = []
        now = datetime.now()
        
        for i in range(10):
            is_income = random.choice([True, False])
            category = random.choice(self.income_categories if is_income else self.expense_categories)
            amount = random.randint(100, 10000) if is_income else -random.randint(100, 5000)
            days_ago = random.randint(0, 10)
            transaction_date = now - timedelta(days=days_ago)
            payment_method = random.choice(['Картка', 'Готівка'])
            description = f"Опис транзакції #{i+1}"
            currency = 'UAH'
            cashback = random.randint(0, 5)
            commission = random.randint(0, 2)
            
            transaction = Transaction(
                transaction_id=f"tr_{random.randint(10000, 99999)}",
                user_id=user.user_id,
                amount=amount,
                date=transaction_date,
                category=category.name,
                description=description,
                is_income=is_income,
                payment_method=payment_method,
                currency=currency,
                cashback=cashback,
                commission=commission
            )
            
            transactions.append(transaction)
        
        return transactions