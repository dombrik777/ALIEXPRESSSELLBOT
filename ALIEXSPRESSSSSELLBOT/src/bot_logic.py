"""Логіка обробки повідомлень та команд Telegram-бота SELL$$."""

from __future__ import annotations

from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, InlineKeyboardButton, InlineKeyboardMarkup, Message

import database as db
from config import BOT_USERNAME, CATEGORIES

router = Router()


def get_main_categories_keyboard() -> InlineKeyboardMarkup:
    """Головне меню: вибір основних розділів (Комплектуючі, Периферія)."""
    keyboard = []
    for key, info in CATEGORIES.items():
        keyboard.append([InlineKeyboardButton(text=info["name"], callback_data=f"group_{key}")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


def get_subcategories_keyboard(group_key: str) -> InlineKeyboardMarkup:
    """Меню підкатегорій для обраного розділу."""
    keyboard = []
    group = CATEGORIES.get(group_key)
    if group:
        for sub_key, sub_info in group["subcategories"].items():
            keyboard.append([InlineKeyboardButton(text=sub_info["name"], callback_data=f"sub_{group_key}_{sub_key}")])
    
    # Кнопка повернення до головного меню
    keyboard.append([InlineKeyboardButton(text="⬅️ Назад до розділів", callback_data="back_to_main")])
    return InlineKeyboardMarkup(inline_keyboard=keyboard)


@router.message(CommandStart())
async def cmd_start(message: Message) -> None:
    """Обробник команди /start."""
    user_id = message.from_user.id
    await db.ensure_user(user_id)

    welcome_text = (
        f"Привіт! Я бот **SELL$$** (`{BOT_USERNAME}`).\n\n"
        "Я моніторю найкращі знижки на AliExpress (від 50% до 75%) у вибраних категоріях.\n\n"
        "Обери розділ нижче:"
    )

    await message.answer(welcome_text, reply_markup=get_main_categories_keyboard(), parse_mode="Markdown")


@router.callback_query(F.data == "back_to_main")
async def process_back_to_main(callback: CallbackQuery) -> None:
    """Повернення до головного меню розділів."""
    await callback.message.edit_text(
        "Обери розділ нижче:",
        reply_markup=get_main_categories_keyboard()
    )
    await callback.answer()


@router.callback_query(F.data.startswith("group_"))
async def process_group_selection(callback: CallbackQuery) -> None:
    """Обробник вибору основного розділу (наприклад, Комплектуючі)."""
    group_key = callback.data.replace("group_", "")
    
    if group_key not in CATEGORIES:
        await callback.answer("Невідомий розділ!", show_alert=True)
        return

    group_name = CATEGORIES[group_key]["name"]
    await callback.message.edit_text(
        f"Ви обрали: **{group_name}**\n\nОбери конкретну категорію:",
        reply_markup=get_subcategories_keyboard(group_key),
        parse_mode="Markdown"
    )
    await callback.answer()


@router.callback_query(F.data.startswith("sub_"))
async def process_subcategory_selection(callback: CallbackQuery) -> None:
    """Обробник вибору конкретної підкатегорії (наприклад, Відеокарти)."""
    parts = callback.data.split("_", 2)
    if len(parts) < 3:
        await callback.answer("Помилка даних!", show_alert=True)
        return
    
    group_key, sub_key = parts[1], parts[2]
    group = CATEGORIES.get(group_key)
    if not group or sub_key not in group["subcategories"]:
        await callback.answer("Категорію не знайдено!", show_alert=True)
        return

    user_id = callback.from_user.id
    sub_info = group["subcategories"][sub_key]
    
    # Зберігаємо повний ключ підкатегорії (наприклад, "components_gpus") у базі
    full_category_key = f"{group_key}_{sub_key}"
    
    await db.ensure_user(user_id)
    await db.set_user_category(user_id, full_category_key)

    await callback.message.edit_text(
        f"Категорію «{sub_info['name']}» успішно збережено!\n\n"
        "Тепер я надсилатиму тобі сповіщення, щойно з'явиться знижка у цьому розділі."
    )
    await callback.answer()