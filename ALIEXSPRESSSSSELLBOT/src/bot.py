"""Точка входу: запуск бота з кореня проєкту командою `py bot.py`."""

from __future__ import annotations

import asyncio
import atexit
import os
import sys

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
BOT_DIR = os.path.join(ROOT_DIR, "aliexpress_bot")
LOCK_FILE = os.path.join(BOT_DIR, ".bot.lock")

sys.path.insert(0, BOT_DIR)
os.chdir(BOT_DIR)


def _acquire_lock() -> None:
    """Не дає запустити другий екземпляр бота (уникає TelegramConflictError)."""
    if os.path.exists(LOCK_FILE):
        with open(LOCK_FILE, encoding="utf-8") as lock_file:
            old_pid = lock_file.read().strip()
        raise RuntimeError(
            "Бот уже запущений.\n"
            f"Зупиніть попередній процес (PID {old_pid}): Ctrl+C у терміналі.\n"
            "Або видаліть файл aliexpress_bot/.bot.lock, якщо бот уже зупинений."
        )

    with open(LOCK_FILE, "w", encoding="utf-8") as lock_file:
        lock_file.write(str(os.getpid()))


def _release_lock() -> None:
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)


from main import main

if __name__ == "__main__":
    _acquire_lock()
    atexit.register(_release_lock)
    try:
        asyncio.run(main())
    finally:
        _release_lock()
