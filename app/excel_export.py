import os
from datetime import datetime
from typing import List

import pandas as pd

from app.models import AppConfig, Item


def _compute_margin_row(item: Item, cfg: AppConfig, platform: str) -> dict:
    fee_rate = cfg.naver_fee_rate if platform == "naver" else cfg.coupang_fee_rate
    total_cost = item.cost_price + cfg.default_extra_cost
    fee = item.sell_price * fee_rate
    margin = item.sell_price - total_cost - fee
    margin_rate = (margin / item.sell_price * 100) if item.sell_price > 0 else 0.0
    return {
        "상품명": item.name,
        "판매가": item.sell_price,
        "원가": item.cost_price,
        "기타비용": cfg.default_extra_cost,
        "수수료(추정)": round(fee, 2),
        "마진": round(margin, 2),
        "마진율(%)": round(margin_rate, 2),
        "소싱처": item.source,
        "소싱 URL": item.url,
        "옵션": item.option_text,
        "메모": item.memo,
    }


def _export_excel(items: List[Item], cfg: AppConfig, platform: str, output_dir: str) -> str:
    os.makedirs(output_dir, exist_ok=True)
    rows = [_compute_margin_row(item, cfg, platform) for item in items]
    df = pd.DataFrame(
        rows,
        columns=[
            "상품명", "판매가", "원가", "기타비용",
            "수수료(추정)", "마진", "마진율(%)",
            "소싱처", "소싱 URL", "옵션", "메모",
        ],
    )
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{platform}_products_{timestamp}.xlsx"
    filepath = os.path.join(output_dir, filename)
    df.to_excel(filepath, index=False)
    return filepath


def export_naver_excel(items: List[Item], cfg: AppConfig, output_dir: str) -> str:
    return _export_excel(items, cfg, "naver", output_dir)


def export_coupang_excel(items: List[Item], cfg: AppConfig, output_dir: str) -> str:
    return _export_excel(items, cfg, "coupang", output_dir)
