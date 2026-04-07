from typing import Optional
from pydantic import BaseModel


class ItemBase(BaseModel):
    name: str = ""
    source: str = ""
    url: str = ""
    cost_price: float = 0.0
    sell_price: float = 0.0
    option_text: str = ""
    memo: str = ""


class ItemCreate(ItemBase):
    pass


class ItemUpdate(BaseModel):
    name: Optional[str] = None
    source: Optional[str] = None
    url: Optional[str] = None
    cost_price: Optional[float] = None
    sell_price: Optional[float] = None
    option_text: Optional[str] = None
    memo: Optional[str] = None


class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True


class AppConfig(BaseModel):
    naver_fee_rate: float = 0.06
    coupang_fee_rate: float = 0.12
    default_extra_cost: float = 0.0


class ConfigUpdate(BaseModel):
    naver_fee_rate: Optional[float] = None
    coupang_fee_rate: Optional[float] = None
    default_extra_cost: Optional[float] = None
