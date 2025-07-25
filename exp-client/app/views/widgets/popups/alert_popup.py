from app.views.widgets.popups.base_popup import BasePopup
from app.utils.language_mapper import LanguageMapper as LM

from app.utils.theme import (
    get_error_color, get_success_color, 
)

class ErrorPopup(BasePopup):
    """Popup for displaying error messages."""
    
    def __init__(self, message, **kwargs):
        super(ErrorPopup, self).__init__(message, **kwargs)
        self.title = LM.message("error_label")
    
    def _get_background_color(self):
        """Get the background color for error popups."""
        return get_error_color()


class SuccessPopup(BasePopup):
    """Popup for displaying success messages."""
    
    def __init__(self, message, **kwargs):
        super(SuccessPopup, self).__init__(message, **kwargs)
        self.title = LM.message("success_label")
    
    def _get_background_color(self):
        """Get the background color for success popups."""
        return get_success_color()