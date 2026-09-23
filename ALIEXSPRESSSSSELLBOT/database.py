"""Асинхронна робота з SQLite через aiosqlite для бота SELL$$."""

from __future__ import annotations

import aiosqlite

from config import DATABASE_PATH


async def init_db() -> None:
    """Створює таблиці, якщо вони ще не існують."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY,
                category TEXT
            );

            CREATE TABLE IF NOT EXISTS notifications (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                category TEXT NOT NULL,
                url TEXT NOT NULL,
                old_price REAL NOT NULL,
                new_price REAL NOT NULL,
                discount REAL NOT NULL,
                notified_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            """
        )
        await db.commit()


async def ensure_user(user_id: int) -> None:
    """Додає користувача в базу, якщо його ще немає."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
            (user_id,),
        )
        await db.commit()


async def set_user_category(user_id: int, category: str) -> None:
    """Зберігає обрану категорію для користувача."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            "UPDATE users SET category = ? WHERE user_id = ?",
            (category, user_id),
        )
        await db.commit()


async def get_user_category(user_id: int) -> str | None:
    """Повертає обрану категорію користувача."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            "SELECT category FROM users WHERE user_id = ?",
            (user_id,),
        )
        row = await cursor.fetchone()
        return row[0] if row and row[0] else None


async def get_users_by_category(category: str) -> list[int]:
    """Повертає список користувачів, що підписані на категорію."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        cursor = await db.execute(
            """
            SELECT user_id FROM users
            WHERE category = ?
            """,
            (category,),
        )
        rows = await cursor.fetchall()
        return [row[0] for row in rows]


async def save_notification(
    category: str,
    url: str,
    old_price: float,
    new_price: float,
    discount: float,
) -> None:
    """Зберігає запис про надіслане сповіщення."""
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.execute(
            """
            INSERT INTO notifications (category, url, old_price, new_price, discount)
            VALUES (?, ?, ?, ?, ?)
            """,
            (category, url, old_price, new_price, discount),
        )
        await db.commit()