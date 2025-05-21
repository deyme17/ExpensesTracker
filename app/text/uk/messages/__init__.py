from .common import COMMON
from .auth import AUTH
from .months import LONG_MONTHS, SHORT_MONTHS
from .analytics import CHART_TYPES, MESSAGES_ANALYTICS
from .bank import BANK

MESSAGES = {
    **COMMON,
    **AUTH,
    **MESSAGES_ANALYTICS,
    **BANK,
    "months": {
        "long": LONG_MONTHS,
        "short": SHORT_MONTHS,
    }
}

CHART_TYPES = CHART_TYPES
