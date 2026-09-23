"""Конфігурація Telegram-бота SELL$$ для моніторингу AliExpress."""

# Username твого бота
BOT_USERNAME = "@ALIEXSPRESSSELLBOT"

# Токен від @BotFather
BOT_TOKEN = "8959733113:AAF4KU6CZ2mHM_XAjL7RLBPWZgUcmgRU0wM"

# Шлях до SQLite-бази даних
DATABASE_PATH = "bot.db"

# Інтервал перевірки цін (30 хвилин)
CHECK_INTERVAL_SECONDS = 30 * 60

# Діапазон знижки для сповіщень (від 50% до 75%)
DISCOUNT_MIN = 50.0
DISCOUNT_MAX = 75.0

# Категорії товарів (без «Смартфони»)
CATEGORIES = {
    "components": {
        "name": "💻 Комплектуючі",
        "subcategories": {
            "gpus": {"name": "Відеокарти", "url": "https://www.aliexpress.com/w/wholesale-%D0%B2%D1%96%D0%B4%D0%B5%D0%BE%D0%BA%D0%B0%D1%80%D1%82%D0%B8-geforce.html?spm=a2g0o.productlist.search.0"},
            "ssds": {"name": "SSD", "url": "https://www.aliexpress.com/w/wholesale-SSD.html?spm=a2g0o.productlist.search.0"},
            "cpus": {"name": "Процесори", "url": "https://www.aliexpress.com/w/wholesale-%D0%9F%D1%80%D0%BE%D1%86%D0%B5%D1%81%D0%BE%D1%80%D0%B8.html?g=y&SearchText=%D0%9F%D1%80%D0%BE%D1%86%D0%B5%D1%81%D0%BE%D1%80%D0%B8&attr=10651-4206381"},
            "rams": {"name": "Оперативна пам'ять", "url": "https://www.aliexpress.com/w/wholesale-%D0%9E%D0%BF%D0%B5%D1%80%D0%B0%D1%82%D0%B8%D0%B2%D0%BD%D0%B0-%D0%BF%D0%B0%D0%BC'%D1%8F%D1%82%D1%8C-DDR4.html?spm=a2g0o.productlist.search.0"},
            "motherboards": {"name": "Материнські плати", "url": "https://www.aliexpress.com/w/wholesale-%D0%9C%D0%B0%D1%82%D0%B5%D1%80%D0%B8%D0%BD%D1%81%D1%8C%D0%BA%D1%96-%D0%BF%D0%BB%D0%B0%D1%82%D0%B8.html?spm=a2g0o.productlist.search.0"},
            "psu": {"name": "Блоки живлення", "url": "https://www.aliexpress.com/w/wholesale-%D0%91%D0%BB%D0%BE%D0%BA%D0%B8-%D0%B6%D0%B8%D0%B2%D0%BB%D0%B5%D0%BD%D0%BD%D1%8F-%D0%B4%D0%BB%D1%8F-%D0%BF%D0%BA.html?spm=a2g0o.productlist.search.0"},
            "cases": {"name": "Корпуси", "url": "https://www.aliexpress.com/w/wholesale-%D0%BA%D0%BE%D1%80%D0%BF%D1%83%D1%81%D0%B8-%D0%B4%D0%BB%D1%8F-%D0%BF%D0%BA.html?spm=a2g0o.productlist.auto_suggest.1.46d8m6jHm6jHwW"},
            "cooling": {"name": "Системи охолодження", "url": "https://www.aliexpress.com/w/wholesale-%D0%A1%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D0%B8-%D0%BE%D1%85%D0%BE%D0%BB%D0%BE%D0%B4%D0%B6%D0%B5%D0%BD%D0%BD%D1%8F-%D0%B4%D0%BB%D1%8F-%D0%BF%D0%BA.html?spm=a2g0o.productlist.search.0"},
        }
    },
    "peripherals": {
        "name": "🎧 Ігрова периферія",
        "subcategories": {
            "headsets": {"name": "Навушники", "url": "https://www.aliexpress.com/w/wholesale-%D0%BD%D0%B0%D1%83%D1%88%D0%BD%D0%B8%D0%BA%D0%B8-razer.html?spm=a2g0o.productlist.search.0L"},
            "mice": {"name": "Ігрові миші", "url": "https://www.aliexpress.com/w/wholesale-%D0%BC%D0%B8%D1%88%D1%96-razer.html?spm=a2g0o.productlist.search.0"},
            "keyboards": {"name": "Ігрові клавіатури", "url": "https://www.aliexpress.com/w/wholesale-%D0%BA%D0%BB%D0%B0%D0%B2%D1%96%D0%B0%D1%82%D1%83%D1%80%D0%B8-razer.html?spm=a2g0o.productlist.search.0"},
            "mousepads": {"name": "Ігрові коврики", "url": "https://www.aliexpress.com/w/wholesale-%D0%86%D0%B3%D1%80%D0%BE%D0%B2%D1%96-%D0%BA%D0%BE%D0%B2%D1%80%D0%B8%D0%BA%D0%B8.html?spm=a2g0o.productlist.search.0"},
            "joysticks": {"name": "Маніпулятори, джойстики", "url": "https://www.aliexpress.com/w/wholesale-%D0%B4%D0%B6%D0%BE%D0%B9%D1%81%D1%82%D0%B8%D0%BA%D0%B8.html?spm=a2g0o.productlist.search.0"},
            "chairs": {"name": "Геймерські крісла", "url": "https://www.aliexpress.com/w/wholesale-%D0%93%D0%B5%D0%B9%D0%BC%D0%B5%D1%80%D1%81%D1%8C%D0%BA%D1%96-%D0%BA%D1%80%D1%96%D1%81%D0%BB%D0%B0.html?spm=a2g0o.productlist.search.0"},
        }
    }
}