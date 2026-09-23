"""Асинхронний парсер списку товарів з AliExpress для бота SELL$$."""

from __future__ import annotations

import json
import re
from dataclasses import dataclass

import aiohttp
from bs4 import BeautifulSoup

from config import DISCOUNT_MAX, DISCOUNT_MIN

HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    ),
    "Accept-Language": "uk-UA,uk;q=0.9,en;q=0.8",
}


@dataclass
class ProductItem:
    """Структура товару зі знижкою."""
    title: str
    link: str
    old_price: float
    new_price: float
    discount: float


async def fetch_category_items(url: str) -> list[ProductItem]:
    """Парсить сторінку категорії AliExpress та знаходить товари із заданою знижкою."""
    timeout = aiohttp.ClientTimeout(total=30)
    discounted_items = []

    try:
        async with aiohttp.ClientSession(headers=HEADERS, timeout=timeout) as session:
            async with session.get(url) as response:
                if response.status != 200:
                    return []
                html = await response.text()
    except Exception:
        return []

    soup = BeautifulSoup(html, "html.parser")
    cards = soup.select(".multi--container--1UZJHLH, [class*='search-card-item']")
    
    for card in cards:
        try:
            title_el = card.select_one("[class*='title'], h1, h2")
            link_el = card.select_one("a")
            price_el = card.select_one("[class*='price'], [class*='salePrice']")
            orig_price_el = card.select_one("[class*='originalPrice'], [class*='del']")

            if not title_el or not link_el or not price_el:
                continue

            title = title_el.get_text(strip=True)
            link = link_el.get("href", "")
            if link.startswith("//"):
                link = "https:" + link

            new_price = float(re.sub(r"[^\d.]", "", price_el.get_text()))
            old_price = float(re.sub(r"[^\d.]", "", orig_price_el.get_text())) if orig_price_el else new_price * 3

            if old_price > new_price:
                discount = 100 - (new_price * 100 / old_price)
                if DISCOUNT_MIN <= discount <= DISCOUNT_MAX:
                    discounted_items.append(
                        ProductItem(
                            title=title,
                            link=link,
                            old_price=old_price,
                            new_price=new_price,
                            discount=discount,
                        )
                    )
        except Exception:
            continue

    return discounted_items