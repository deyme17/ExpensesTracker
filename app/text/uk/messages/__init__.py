from .transaction import TRANSACTION
from .filter_sort import FILTER_SORT
from .buttons import BUTTONS
from .status import STATUS
from .account import ACCOUNT
from .analytics import ANALYTICS
from .auth import AUTH
from .menu import MENU
from .bank import BANK

MESSAGES = {
    **TRANSACTION,
    **FILTER_SORT,
    **BUTTONS,
    **STATUS,
    **ACCOUNT,
    **ANALYTICS,
    **AUTH,
    **MENU,
    **BANK,
}
