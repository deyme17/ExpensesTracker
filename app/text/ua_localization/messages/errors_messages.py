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

    # System-side (unexpected or backend issues)
    "server_unreachable": "Сервер недоступний. Перевірте підключення до інтернету",
    "offline_mode": "Ви працюєте в офлайн-режимі. Деякі функції можуть бути недоступні",
    "timeout": "Перевищено час очікування відповіді",
    "db_error": "Виникла помилка при роботі з базою даних",
    "unknown_error": "Несподівана помилка. Будь ласка, спробуйте ще раз",
    "transaction_not_found": "Транзакцію не знайдено",
    "access_denied": "У вас немає доступу до цієї інформації"
}
