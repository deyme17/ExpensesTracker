# Application information
APP_NAME = "ExpensesTracker"
APP_TITLE = APP_NAME
APP_VERSION = "1.0.0"

# months
SHORT_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
LONG_MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"]

# Currency codes
CURRENCY_UAH = "UAH"
CURRENCY_USD = "USD"
CURRENCY_EUR = "EUR"

TRANSACTION_TYPES = ["all", "income", "expense"]
PAYMENT_METHODS = ["all", "card", "cash"]

# charts
CHART_TYPE_PIE = "pie"
CHART_TYPE_HISTOGRAM = "histogram"
CHART_TYPE_LINE = "line"

# sorting fields
SORT_FIELDS = ['date', 'amount', 'cashback', 'commission']

# Default currency
DEFAULT_CURRENCY = CURRENCY_UAH

CATEGORIES = ['groceries', 'transport', 'entertainment', 'healthcare', 
              'clothing', 'cafe', 'connection', 'other']    # TODO delete this
MCC_MAPPING = {                                             # TODO delete this
    # Food & Supermarkets
    5411: 'groceries',   # Grocery stores & Supermarkets
    5422: 'groceries',   # Meat/Fish Stores
    5441: 'groceries',   # Candy/Nut/Confectionery Stores
    5451: 'groceries',   # Dairy Products Stores
    5462: 'groceries',   # Bakeries
    5499: 'groceries',   # Misc. Food Stores
    
    # Transportation
    4111: 'transport',  # Local/Suburban Transit
    4112: 'transport',  # Passenger Railways
    4121: 'transport',  # Taxicabs/Limousines
    4131: 'transport',  # Bus Lines
    4784: 'transport',  # Tolls/Bridge Fees
    5541: 'transport',  # Service Stations
    5542: 'transport',  # Automated Fuel Dispensers
    
    # Entertainment
    7832: 'entertainment',    # Motion Picture Theaters
    7841: 'entertainment',    # Video Rental Stores
    7911: 'entertainment',    # Dance Halls/Studios/Schools
    7922: 'entertainment',    # Theatrical Producers
    7929: 'entertainment',    # Bands, Orchestras, Entertainment
    7932: 'entertainment',    # Billiard/Pool Establishments
    7941: 'entertainment',    # Commercial Sports
    7991: 'entertainment',    # Tourist Attractions and Exhibits
    7994: 'entertainment',    # Video Game Arcades
    7995: 'entertainment',    # Gambling Transactions
    7996: 'entertainment',    # Amusement Parks, Carnivals, Circuses
    7998: 'entertainment',    # Aquariums, Seaquariums
    7999: 'entertainment',    # Recreation Services
    
    # Healthcare
    4119: 'healthcare',   # Ambulance Services
    5912: 'healthcare',   # Drug Stores/Pharmacies
    5975: 'healthcare',   # Hearing Aids
    5976: 'healthcare',   # Orthopedic Goods/Prosthetic Devices
    8011: 'healthcare',   # Doctors
    8021: 'healthcare',   # Dentists, Orthodontists
    8031: 'healthcare',   # Osteopaths
    8041: 'healthcare',   # Chiropractors
    8042: 'healthcare',   # Optometrists, Ophthalmologists
    8043: 'healthcare',   # Opticians, Optical Goods
    8049: 'healthcare',   # Podiatrists, Chiropodists
    8050: 'healthcare',   # Nursing/Personal Care Facilities
    8062: 'healthcare',   # Hospitals
    8071: 'healthcare',   # Medical and Dental Labs
    8099: 'healthcare',   # Medical Services
    
    # Clothing
    5611: 'clothing',       # Men's and Boy's Clothing and Accessories
    5621: 'clothing',       # Women's Ready-to-Wear Stores
    5631: 'clothing',       # Women's Accessory and Specialty Shops
    5641: 'clothing',       # Children's and Infant's Wear Stores
    5651: 'clothing',       # Family Clothing Stores
    5655: 'clothing',       # Sports and Riding Apparel Stores
    5661: 'clothing',       # Shoe Stores
    5681: 'clothing',       # Furriers and Fur Shops
    5691: 'clothing',       # Men's and Women's Clothing Stores
    5699: 'clothing',       # Miscellaneous Apparel and Accessory Shops
    
    # Restaurants/Cafes
    5812: 'cafe',       # Eating Places, Restaurants
    5813: 'cafe',       # Drinking Places (Alcoholic Beverages)
    5814: 'cafe',       # Fast Food Restaurants
    
    # Telecommunications
    4814: 'connection',    # Telecommunication Services
    4815: 'connection',    # Monthly Summary Telephone Charges
    4816: 'connection',    # Computer Network Services
    4821: 'connection',    # Telegraph Services
    4899: 'connection',    # Cable and other Pay Television Services
    
    # default
    0: 'other'        
}

CURRENCY_CODE_MAPPING = {                       # TODO delete this
    980: "UAH",  # Українська гривня
    840: "USD",  # Долар США
    978: "EUR",  # Євро
    826: "GBP",  # Фунт стерлінгів
    985: "PLN",  # Польський злотий
    933: "BYN",  # Білоруський рубль
    643: "RUB",  # Російський рубль
    124: "CAD",  # Канадський долар
    203: "CZK",  # Чеська крона
    348: "HUF",  # Угорський форинт
    756: "CHF",  # Швейцарський франк
    392: "JPY",  # Японська єна
    156: "CNY",  # Китайський юань
    36:  "AUD",  # Австралійський долар
    578: "NOK",  # Норвезька крона
    752: "SEK",  # Шведська крона
    208: "DKK",  # Данська крона
    0:   "UAH"   # За замовчуванням — гривня
}
