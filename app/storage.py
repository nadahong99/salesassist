import json
import os
from typing import List

from app.models import AppConfig, Item

DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
ITEMS_FILE = os.path.join(DATA_DIR, "items.json")
CONFIG_FILE = os.path.join(DATA_DIR, "config.json")

_DEFAULT_CONFIG = {"naver_fee_rate": 0.06, "coupang_fee_rate": 0.12, "default_extra_cost": 0.0}


def _ensure_data_dir() -> None:
    os.makedirs(DATA_DIR, exist_ok=True)
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "w", encoding="utf-8") as f:
            json.dump(_DEFAULT_CONFIG, f, ensure_ascii=False, indent=2)
    if not os.path.exists(ITEMS_FILE):
        with open(ITEMS_FILE, "w", encoding="utf-8") as f:
            json.dump([], f)


def load_items() -> List[Item]:
    _ensure_data_dir()
    with open(ITEMS_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return [Item(**row) for row in data]


def save_items(items: List[Item]) -> None:
    _ensure_data_dir()
    with open(ITEMS_FILE, "w", encoding="utf-8") as f:
        json.dump([item.model_dump() for item in items], f, ensure_ascii=False, indent=2)


def load_config() -> AppConfig:
    _ensure_data_dir()
    with open(CONFIG_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)
    return AppConfig(**data)


def save_config(config: AppConfig) -> None:
    _ensure_data_dir()
    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(config.model_dump(), f, ensure_ascii=False, indent=2)
