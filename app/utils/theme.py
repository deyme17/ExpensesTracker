from kivy.utils import get_color_from_hex

# base colors
PRIMARY_COLOR = '#0A4035'  # Dark teal
SECONDARY_COLOR = '#D8F3EB'  # Light teal
ACCENT_COLOR = '#FF7043'  # Orange
ERROR_COLOR = '#8B0000'  # Dark red
SUCCESS_COLOR = '#35884D'  # Green
BACKGROUND_COLOR = '#0F7055'  # Medium teal

# color functions
def get_primary_color(alpha=1.0):
    """Get primary color with specified alpha."""
    color = get_color_from_hex(PRIMARY_COLOR)
    return (color[0], color[1], color[2], alpha)

def get_secondary_color(alpha=1.0):
    """Get secondary color with specified alpha."""
    color = get_color_from_hex(SECONDARY_COLOR)
    return (color[0], color[1], color[2], alpha)

def get_accent_color(alpha=1.0):
    """Get accent color with specified alpha."""
    color = get_color_from_hex(ACCENT_COLOR)
    return (color[0], color[1], color[2], alpha)

def get_error_color(alpha=1.0):
    """Get error color with specified alpha."""
    color = get_color_from_hex(ERROR_COLOR)
    return (color[0], color[1], color[2], alpha)

def get_success_color(alpha=1.0):
    """Get success color with specified alpha."""
    color = get_color_from_hex(SUCCESS_COLOR)
    return (color[0], color[1], color[2], alpha)

def get_background_color(alpha=1.0):
    """Get background color with specified alpha."""
    color = get_color_from_hex(BACKGROUND_COLOR)
    return (color[0], color[1], color[2], alpha)

INCOME_COLOR = '#35884D'  # green for income
EXPENSE_COLOR = '#A83C36'  # red for expenses

def get_income_color(alpha=1.0):
    """Get income color with specified alpha."""
    color = get_color_from_hex(INCOME_COLOR)
    return (color[0], color[1], color[2], alpha)

def get_expense_color(alpha=1.0):
    """Get expense color with specified alpha."""
    color = get_color_from_hex(EXPENSE_COLOR)
    return (color[0], color[1], color[2], alpha)

# text colors
TEXT_PRIMARY = '#FFFFFF'  # white
TEXT_SECONDARY = '#D8F3EB'  # light teal
TEXT_DARK = '#0A4035'  # dark teal

def get_text_primary_color(alpha=1.0):
    """Get primary text color with specified alpha."""
    color = get_color_from_hex(TEXT_PRIMARY)
    return (color[0], color[1], color[2], alpha)

def get_text_secondary_color(alpha=1.0):
    """Get secondary text color with specified alpha."""
    color = get_color_from_hex(TEXT_SECONDARY)
    return (color[0], color[1], color[2], alpha)

def get_text_dark_color(alpha=1.0):
    """Get dark text color with specified alpha."""
    color = get_color_from_hex(TEXT_DARK)
    return (color[0], color[1], color[2], alpha)

# category colors for charts
CATEGORY_COLORS = [
    '#FF7043',  # orange
    '#FFB74D',  # light orange
    '#FFF176',  # yellow
    '#AED581',  # light green
    '#4CAF50',  # green
    '#26A69A',  # teal
    '#29B6F6',  # light blue
    '#5C6BC0',  # indigo
    '#7E57C2',  # purple
    '#EC407A',  # pink
    '#EF5350',  # red
    '#8D6E63',  # brown
]

def get_category_color(index, alpha=1.0):
    """
    Get a color for a category by index.
    
    Args:
        index (int): Category index
        alpha (float): Alpha value
        
    Returns:
        tuple: (r, g, b, a) color tuple
    """
    color_index = index % len(CATEGORY_COLORS)
    color = get_color_from_hex(CATEGORY_COLORS[color_index])
    return (color[0], color[1], color[2], alpha)

# font sizes
FONT_SIZE_SMALL = 14
FONT_SIZE_MEDIUM = 16
FONT_SIZE_LARGE = 18
FONT_SIZE_EXTRA_LARGE = 22
FONT_SIZE_TITLE = 24

# stats colors
STAT_COLORS = {
    'avg': get_color_from_hex('#E09B40'),        # помаранч
    'min': get_color_from_hex('#4DD0E1'),        # блакитний
    'max': get_color_from_hex('#EF5350'),        # червоний
    'total': get_color_from_hex('#AED581'),      # лайм
    'count': get_color_from_hex('#CFD8DC'),      # білий
    'top_category': get_color_from_hex('#FFF176') #  жовтий
}