import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

ITEMS_FILE = DATA_DIR / "items.json"
CONFIG_FILE = DATA_DIR / "config.json"
RECEIPTS_FILE = DATA_DIR / "receipts.json"

_DEFAULT_CONFIG = {
    "naver_commission": 3.5,
    "coupang_commission": 5.0,
    "shipping_cost": 3000,
    "other_cost": 0,
    "target_margin": 20.0,
    "tax_rate": 0.0,
}


def _read(path: Path, default: Any) -> Any:
    if not path.exists():
        return default
    with open(path, encoding="utf-8") as f:
        return json.load(f)


def _write(path: Path, data: Any) -> None:
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def load_items() -> list:
    return _read(ITEMS_FILE, [])


def save_items(items: list) -> None:
    _write(ITEMS_FILE, items)


def load_config() -> dict:
    stored = _read(CONFIG_FILE, {})
    return {**_DEFAULT_CONFIG, **stored}


def save_config(config: dict) -> None:
    _write(CONFIG_FILE, config)


def next_id(items: list) -> int:
    if not items:
        return 1
    return max(it["id"] for it in items) + 1


def load_receipts() -> list:
    return _read(RECEIPTS_FILE, [])


def save_receipts(receipts: list) -> None:
    _write(RECEIPTS_FILE, receipts)
