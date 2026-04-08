from typing import Optional
from pydantic import BaseModel, Field


class Config(BaseModel):
    naver_commission: float = Field(default=3.5, description="네이버 수수료 (%)")
    coupang_commission: float = Field(default=5.0, description="쿠팡 수수료 (%)")
    shipping_cost: float = Field(default=3000, description="배송비 (원)")
    other_cost: float = Field(default=0, description="기타비용 (원)")
    target_margin: float = Field(default=20.0, description="목표 마진율 (%)")
    tax_rate: float = Field(default=0.0, description="부가세율 (%) - 0이면 미적용")


class ItemCreate(BaseModel):
    name: str = Field(..., description="상품명")
    purchase_price: float = Field(..., ge=0, description="매입가 (원)")
    naver_price: Optional[float] = Field(default=None, ge=0, description="네이버 판매가 (원)")
    coupang_price: Optional[float] = Field(default=None, ge=0, description="쿠팡 판매가 (원)")
    source: Optional[str] = Field(default="", description="소싱처")
    url: Optional[str] = Field(default="", description="소싱 URL")
    memo: Optional[str] = Field(default="", description="메모")


class Item(ItemCreate):
    id: int


class ReceiptCreate(BaseModel):
    date: str = Field(..., description="날짜 (YYYY-MM-DD)")
    vendor: str = Field(..., description="거래처/상호")
    description: str = Field(default="", description="품목/내용")
    amount: float = Field(..., ge=0, description="공급가액 (원, 세전)")
    tax_amount: float = Field(default=0.0, ge=0, description="부가세 (원)")
    receipt_type: str = Field(default="매입", description="유형: 매입/매출/기타")
    memo: Optional[str] = Field(default="", description="메모")


class Receipt(ReceiptCreate):
    id: int
