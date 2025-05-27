ERRORS = {
    # Monobank/API-related
    "too_many_requests": "Monobank тимчасово обмежив доступ. Спробуйте пізніше.",
    "client_info_error": "Помилка отримання клієнтської інформації: {status} – {text}",
    "transactions_fetch_error": "Помилка отримання транзакцій: {status} – {text}",
    "missing_account_id": "Не вказано account_id для запиту транзакцій.",
    "no_accounts_found": "У Monobank не знайдено жодного акаунту.",

    # User-side (expected input errors)
    "user_exists": "Користувач з таким email вже існує",
    "user_not_found": "Користувача не знайдено",
    "invalid_credentials": "Невірний email або пароль",
    "token_missing": "Відсутній токен для авторизації",
    "registration_not_supported_local": "Реєстрація недоступна в офлайн-режимі",
    "invalid_token_format": "Невірний формат токену Monobank",
    "registration_failed": "Помилка під час реєстрації: {error}",

    # Input validation (form fields)
    "email_required": "Email обов’язковий",
    "email_invalid": "Некоректний email",
    "password_required": "Пароль обов’язковий",
    "password_too_short": "Пароль має містити щонайменше 6 символів",
    "password_needs_digit": "Пароль повинен містити щонайменше одну цифру",
    "password_needs_letter": "Пароль повинен містити щонайменше одну літеру",
    "password_mismatch": "Паролі не співпадають",
    "amount_required": "Поле суми обов’язкове",
    "nonzero_amount": "Сума не може дорівнювати нулю",
    "positive_cashback": "Кешбек не може бути від’ємним",
    "positive_commission": "Комісія не може бути від’ємною",

    # System-side (unexpected or backend issues)
    "server_unreachable": "Сервер недоступний. Перевірте підключення до інтернету",
    "offline_mode": "Ви працюєте в офлайн-режимі. Деякі функції можуть бути недоступні",
    "timeout": "Перевищено час очікування відповіді",
    "db_error": "Виникла помилка при роботі з базою даних",
    "unknown_error": "Несподівана помилка. Будь ласка, спробуйте ще раз",
    "transaction_not_found": "Транзакцію не знайдено",
    "access_denied": "У вас немає доступу до цієї інформації"
}
