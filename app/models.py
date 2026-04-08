from typing import Optional
from pydantic import BaseModel, Field, field_validator


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

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: Optional[str]) -> Optional[str]:
        if not v:
            return v
        if v.startswith("http://") or v.startswith("https://"):
            return v
        raise ValueError("소싱 URL은 http:// 또는 https://로 시작해야 합니다.")


class Item(ItemCreate):
    id: int
