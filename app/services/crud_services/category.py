from app.api import api_get_categories
from app.utils.constants import DEFAULT_MCC, DEFAULT_CATEGORY
from app.utils.error_codes import ErrorCodes
from app.models.category import Category


class CategoryService:
    """
    Handles category data operations including MCC code lookups and caching.
    Args:
        storage_service: Optional storage service for local caching (must implement 
                         `save_categories()` and `get_categories()`)
    """
    def __init__(self, storage_service=None):
        self.storage_service = storage_service
        self._mcc_to_name = {}
        self._name_to_mcc = {}

    def get_categories(self) -> tuple[list, str]:
        """
        Retrieves categories from cache, API, or local storage (in priority order).
        Returns:
            Tuple: (list_of_categories, error_message)
        """
        if self._mcc_to_name:
            return [Category(mcc_code=k, name=v) for k, v in self._mcc_to_name.items()], None

        try:
            result = api_get_categories()

            if result.get("success"):
                categories = [Category.from_dict(c) for c in result["data"]]

                if self.storage_service:
                    self.storage_service.categories.save_categories(categories)

                self._update_category_cache(categories)
                return categories, None
            
            return [], result.get("error", ErrorCodes.UNKNOWN_ERROR)
        except Exception:
            pass

        if self.storage_service:
            categories = self.storage_service.categories.get_categories()
            self._update_category_cache(categories)
            return categories, ErrorCodes.OFFLINE_MODE

        return [], ErrorCodes.UNKNOWN_ERROR

    def _update_category_cache(self, categories: list):
        """
        Updates internal MCC/category name mappings.
        Args:
            categories: List of category model instances
        """
        self._mcc_to_name = {c.mcc_code: c.name for c in categories}
        self._name_to_mcc = {v: k for k, v in self._mcc_to_name.items()}

    def get_category_name_by_mcc(self, mcc_code: str|int) -> str:
        """
        Gets category name for given MCC code.
        Args:
            mcc_code: Integer MCC code
        Returns:
            str: Category name or DEFAULT_CATEGORY if not found
        """
        if not self._mcc_to_name:
            categories, _ = self.get_categories()
            self._update_category_cache(categories)

        return self._mcc_to_name.get(int(mcc_code), DEFAULT_CATEGORY)

    def get_mcc_by_name(self, name: str) -> str:
        """
        Gets MCC code for given category name.
        Args:
            name: Category name string
        Returns:
            int: MCC code or DEFAULT_MCC if not found
        """
        if not self._name_to_mcc:
            categories, _ = self.get_categories()
            self._update_category_cache(categories)

        return str(self._name_to_mcc.get(name, DEFAULT_MCC))