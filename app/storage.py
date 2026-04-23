import json
from pathlib import Path
from typing import Any

DATA_DIR = Path(__file__).parent.parent / "data"
DATA_DIR.mkdir(exist_ok=True)

ITEMS_FILE = DATA_DIR / "items.json"
CONFIG_FILE = DATA_DIR / "config.json"
ORDERS_FILE = DATA_DIR / "orders.json"

_DEFAULT_CONFIG = {
    "naver_commission": 3.5,
    "coupang_commission": 5.0,
    "shipping_cost": 3000,
    "other_cost": 0,
    "target_margin": 20.0,
    "tax_rate": 0.0,
}

# 상품 데이터 기본값 (신규 필드의 하위 호환성 보장)
_ITEM_DEFAULTS = {
    "source_type": "해외",
    "wholesale_price": None,
    "min_order_qty": None,
    "has_customs_tax": False,
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
    items = _read(ITEMS_FILE, [])
    # 기존 데이터에 신규 필드 기본값 보완 (하위 호환)
    for item in items:
        for key, default in _ITEM_DEFAULTS.items():
            if key not in item:
                item[key] = default
        checklist = item.get("return_checklist", {})
        if "tax_invoice_issued" not in checklist:
            checklist["tax_invoice_issued"] = False
        item["return_checklist"] = checklist
    return items


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


def load_orders() -> list:
    return _read(ORDERS_FILE, [])


def save_orders(orders: list) -> None:
    _write(ORDERS_FILE, orders)
