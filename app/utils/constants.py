# Application information
APP_NAME = "ExpensesTracker"
APP_TITLE = "ExpensesTracker - Фінансовий моніторинг"
APP_VERSION = "1.0.0"

# Transaction types
TRANSACTION_TYPE_INCOME = "Доходи"
TRANSACTION_TYPE_EXPENSE = "Витрати"
TRANSACTION_TYPE_ALL = "Всі"

# Payment methods
PAYMENT_METHOD_CARD = "Картка"
PAYMENT_METHOD_CASH = "Готівка"
PAYMENT_METHOD_ALL = "Всі"

# Currency codes
CURRENCY_UAH = "UAH"
CURRENCY_USD = "USD"
CURRENCY_EUR = "EUR"

# Default currency
DEFAULT_CURRENCY = CURRENCY_UAH

# Chart types
CHART_TYPE_HISTOGRAM = "histogram"
CHART_TYPE_PIE = "pie"
CHART_TYPE_LINE = "line"

# Income categories    # TODO
INCOME_CATEGORIES = [
    'Зарплата',
    'Подарунок',
    'Дивіденди',
    'Фріланс',
    'Відсотки',
    'Інше'
]

# Expense categories    # TODO
EXPENSE_CATEGORIES = [
    'Продукти',
    'Транспорт',
    'Розваги',
    'Здоров\'я',
    'Одяг',
    'Кафе',
    'Зв\'язок',
    'Інше'
]

# MCC code mappings (Merchant Category Codes)
# Maps MCC codes from banks to our expense categories
MCC_MAPPING = {
    # Food & Supermarkets
    5411: 'Продукти',   # Grocery stores & Supermarkets
    5422: 'Продукти',   # Meat/Fish Stores
    5441: 'Продукти',   # Candy/Nut/Confectionery Stores
    5451: 'Продукти',   # Dairy Products Stores
    5462: 'Продукти',   # Bakeries
    5499: 'Продукти',   # Misc. Food Stores
    
    # Transportation
    4111: 'Транспорт',  # Local/Suburban Transit
    4112: 'Транспорт',  # Passenger Railways
    4121: 'Транспорт',  # Taxicabs/Limousines
    4131: 'Транспорт',  # Bus Lines
    4784: 'Транспорт',  # Tolls/Bridge Fees
    5541: 'Транспорт',  # Service Stations
    5542: 'Транспорт',  # Automated Fuel Dispensers
    
    # Entertainment
    7832: 'Розваги',    # Motion Picture Theaters
    7841: 'Розваги',    # Video Rental Stores
    7911: 'Розваги',    # Dance Halls/Studios/Schools
    7922: 'Розваги',    # Theatrical Producers
    7929: 'Розваги',    # Bands, Orchestras, Entertainment
    7932: 'Розваги',    # Billiard/Pool Establishments
    7941: 'Розваги',    # Commercial Sports
    7991: 'Розваги',    # Tourist Attractions and Exhibits
    7994: 'Розваги',    # Video Game Arcades
    7995: 'Розваги',    # Gambling Transactions
    7996: 'Розваги',    # Amusement Parks, Carnivals, Circuses
    7998: 'Розваги',    # Aquariums, Seaquariums
    7999: 'Розваги',    # Recreation Services
    
    # Healthcare
    4119: 'Здоров\'я',   # Ambulance Services
    5912: 'Здоров\'я',   # Drug Stores/Pharmacies
    5975: 'Здоров\'я',   # Hearing Aids
    5976: 'Здоров\'я',   # Orthopedic Goods/Prosthetic Devices
    8011: 'Здоров\'я',   # Doctors
    8021: 'Здоров\'я',   # Dentists, Orthodontists
    8031: 'Здоров\'я',   # Osteopaths
    8041: 'Здоров\'я',   # Chiropractors
    8042: 'Здоров\'я',   # Optometrists, Ophthalmologists
    8043: 'Здоров\'я',   # Opticians, Optical Goods
    8049: 'Здоров\'я',   # Podiatrists, Chiropodists
    8050: 'Здоров\'я',   # Nursing/Personal Care Facilities
    8062: 'Здоров\'я',   # Hospitals
    8071: 'Здоров\'я',   # Medical and Dental Labs
    8099: 'Здоров\'я',   # Medical Services
    
    # Clothing
    5611: 'Одяг',       # Men's and Boy's Clothing and Accessories
    5621: 'Одяг',       # Women's Ready-to-Wear Stores
    5631: 'Одяг',       # Women's Accessory and Specialty Shops
    5641: 'Одяг',       # Children's and Infant's Wear Stores
    5651: 'Одяг',       # Family Clothing Stores
    5655: 'Одяг',       # Sports and Riding Apparel Stores
    5661: 'Одяг',       # Shoe Stores
    5681: 'Одяг',       # Furriers and Fur Shops
    5691: 'Одяг',       # Men's and Women's Clothing Stores
    5699: 'Одяг',       # Miscellaneous Apparel and Accessory Shops
    
    # Restaurants/Cafes
    5812: 'Кафе',       # Eating Places, Restaurants
    5813: 'Кафе',       # Drinking Places (Alcoholic Beverages)
    5814: 'Кафе',       # Fast Food Restaurants
    
    # Telecommunications
    4814: 'Зв\'язок',    # Telecommunication Services
    4815: 'Зв\'язок',    # Monthly Summary Telephone Charges
    4816: 'Зв\'язок',    # Computer Network Services
    4821: 'Зв\'язок',    # Telegraph Services
    4899: 'Зв\'язок',    # Cable and other Pay Television Services
    
    # default
    0: 'Інше'        
}