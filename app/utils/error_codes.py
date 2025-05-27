class ErrorCodes:
    # Monobank/API-related
    TOO_MANY_REQUESTS = "too_many_requests"
    CLIENT_INFO_ERROR = "client_info_error"
    TRANSACTIONS_FETCH_ERROR = "transactions_fetch_error"
    MISSING_ACCOUNT_ID = "missing_account_id"
    NO_ACCOUNTS_FOUND = "no_accounts_found"

    # User-side
    USER_EXISTS = "user_exists"
    USER_NOT_FOUND = "user_not_found"
    INVALID_CREDENTIALS = "invalid_credentials"
    TOKEN_MISSING = "token_missing"
    REGISTRATION_NOT_SUPPORTED_LOCAL = "registration_not_supported_local"
    INVALID_TOKEN_FORMAT = "invalid_token_format"
    REGISTRATION_FAILED = "registration_failed"
    INVALID_DATE_FORMAT = "invalid_date_format"

    # System-side
    SERVER_UNREACHABLE = "server_unreachable"
    OFFLINE_MODE = "offline_mode"
    TIMEOUT = "timeout"
    DB_ERROR = "db_error"
    UNKNOWN_ERROR = "unknown_error"
    TRANSACTION_NOT_FOUND = "transaction_not_found"
    ACCESS_DENIED = "access_denied"
