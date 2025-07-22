class ErrorCodes:
    # Monobank/API-related
    TOO_MANY_REQUESTS = "Забагато запитів. Спробуйте пізніше."
    CLIENT_INFO_ERROR = "Помилка інформації про клієнта."
    TRANSACTIONS_FETCH_ERROR = "Не вдалося отримати транзакції."
    MISSING_ACCOUNT_ID = "Відсутній ідентифікатор рахунку."
    NO_ACCOUNTS_FOUND = "Рахунки не знайдено."
    API_FAILED_BUT_LOADED_LOCAL = "API не працює, використано локальні дані."
    UNAUTHORIZED = "Неавторизовано. Увійдіть у систему."
    FORBIDDEN = "Доступ заборонено."
    BAD_REQUEST = "Неправильний запит."
    INVALID_RESPONSE = "Невірна відповідь від сервера."

    # User-side
    USER_EXISTS = "Користувач уже існує."
    USER_NOT_FOUND = "Користувача не знайдено."
    INVALID_CREDENTIALS = "Неправильні логін або пароль."
    TOKEN_MISSING = "Відсутній токен авторизації."
    REGISTRATION_NOT_SUPPORTED_LOCAL = "Реєстрація недоступна в локальному режимі."
    INVALID_TOKEN_FORMAT = "Невірний формат токена."
    REGISTRATION_FAILED = "Помилка реєстрації."
    INVALID_DATE_FORMAT = "Неправильний формат дати."

    # System-side
    SERVER_UNREACHABLE = "Сервер недоступний."
    OFFLINE_MODE = "Режим офлайн."
    TIMEOUT = "Час очікування минув."
    DB_ERROR = "Помилка бази даних."
    UNKNOWN_ERROR = "Невідома помилка."
    TRANSACTION_NOT_FOUND = "Транзакцію не знайдено."
    ACCESS_DENIED = "Доступ заборонено."
