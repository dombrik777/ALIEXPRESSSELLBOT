import asyncio
import logging
import requests
from threading import Thread
from flask import Flask
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# ==========================================
# ЧАСТИНА 0: МІКРО-СЕРВЕР ДЛЯ RENDER (FLASK)
# ==========================================
app = Flask('')

@app.route('/')
def home():
    return "Бот працює 24/7!"

def run_flask():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_flask)
    t.start()


# ==========================================
# ЧАСТИНА 1: НАЛАШТУВАННЯ ТА КЛЮЧІ
# ==========================================
BOT_TOKEN = "8959733113:AAF4KU6CZ2mHM_XAjL7RLBPWZgUcmgRU0wM"
RAPIDAPI_KEY = "c90ddde9dfmsh7a4a6c1447b3a80p1809cbjsn736e6def9d3f"

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
logging.basicConfig(level=logging.INFO)


# ==========================================
# ЧАСТИНА 2: ПАМ'ЯТЬ БОТА
# ==========================================
user_subscriptions = {}


# ==========================================
# ЧАСТИНА 3: СТВОРЕННЯ КЛАВІАТУР
# ==========================================
def get_products_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🖱 Миші Razer", callback_data="track_mouse razer")],
        [InlineKeyboardButton(text="🎧 Навушники", callback_data="track_headphones")],
        [InlineKeyboardButton(text="⌨️ Механічні клавіатури", callback_data="track_mechanical keyboard")],
        [InlineKeyboardButton(text="💻 SSD Накопичувачі", callback_data="track_ssd 1tb")]
    ])
    return keyboard

def get_stop_keyboard():
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛑 Припинити пошук", callback_data="stop_tracking")]
    ])
    return keyboard


# ==========================================
# ЧАСТИНА 4: ОБРОБКА КОМАНД ТА КНОПОК
# ==========================================
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer("Привіт! Натисни /menu, щоб вибрати товари для відстеження знижок.")

@dp.message(Command("menu"))
async def show_menu(message: types.Message):
    await message.answer(
        "Вибери категорію товару, і я буду надсилати тобі пропозиції зі знижками (50-75%):", 
        reply_markup=get_products_keyboard()
    )

@dp.callback_query(F.data.startswith("track_"))
async def handle_product_selection(callback: types.CallbackQuery):
    product_name = callback.data.replace("track_", "")
    user_id = callback.from_user.id
    
    if user_id in user_subscriptions and user_subscriptions[user_id] is not None:
        current_product = user_subscriptions[user_id]
        await callback.message.answer(
            f"⚠️ Ти вже шукаєш знижки на: <b>{current_product}</b>!\n\n"
            f"Спочатку припини поточний пошук:",
            reply_markup=get_stop_keyboard(),
            parse_mode="HTML"
        )
    else:
        user_subscriptions[user_id] = product_name
        await callback.message.answer(
            f"✅ Відмінний вибір! Я почав шукати знижки на: <b>{product_name}</b>\n\n"
            f"Якщо передумаєш або захочеш змінити категорію, натисни кнопку нижче.", 
            reply_markup=get_stop_keyboard(),
            parse_mode="HTML"
        )
        
    await callback.answer()

@dp.callback_query(F.data == "stop_tracking")
async def handle_stop_tracking(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    if user_id in user_subscriptions:
        del user_subscriptions[user_id]
        
    await callback.message.answer(
        "🛑 Пошук успішно припинено!\nТепер ти можеш вибрати нову категорію через /menu."
    )
    await callback.answer()


# ==========================================
# ЧАСТИНА 5: ФОНОВА ПЕРЕВІРКА ЦІН
# ==========================================
async def check_prices_background():
    while True:
        for user_id, product_name in list(user_subscriptions.items()):
            try:
                url = "https://aliexpress-datahub.p.rapidapi.com/item_search_3"
                querystring = {"q": product_name, "page": "1"}
                headers = {
                    "x-rapidapi-key": RAPIDAPI_KEY,
                    "x-rapidapi-host": "aliexpress-datahub.p.rapidapi.com"
                }
                
                response = requests.get(url, headers=headers, params=querystring)
                data = response.json()
                
                items = data.get("result", {}).get("resultList", [])
                
                for entry in items:
                    item_info = entry.get("item", {})
                    sku_def = item_info.get("sku", {}).get("def", {})
                    old_price = sku_def.get("price")
                    new_price = sku_def.get("promotionPrice")
                    
                    title = item_info.get("title", "Товар без назви")
                    item_url = item_info.get("itemUrl", "")
                    
                    if item_url.startswith("//"):
                        item_url = "https:" + item_url
                        
                    if old_price is not None and new_price is not None and old_price > 0:
                        discount_percent = 100 - (new_price / old_price * 100)
                        
                        if 50 <= discount_percent <= 75:
                            message_text = (
                                f"🔥 <b>Знайдено знижку! (-{int(discount_percent)}%)</b>\n\n"
                                f"📦 <b>Назва:</b> {title}\n"
                                f"❌ <b>Стара ціна:</b> ${old_price}\n"
                                f"✅ <b>Нова ціна:</b> ${new_price}\n\n"
                                f"🔗 <a href='{item_url}'>Перейти на AliExpress</a>"
                            )
                            
                            await bot.send_message(user_id, message_text, reply_markup=get_stop_keyboard(), parse_mode="HTML")
                            
            except Exception as e:
                logging.error(f"Помилка для користувача {user_id} по товару {product_name}: {e}")
            
            await asyncio.sleep(2)
            
        await asyncio.sleep(10800) 


# ==========================================
# ЧАСТИНА 6: ЗАПУСК
# ==========================================
async def main():
    asyncio.create_task(check_prices_background())
    await dp.start_polling(bot)

if __name__ == "__main__":
    keep_alive()  # Запускаємо сервер Flask у фоновому потоці
    asyncio.run(main())