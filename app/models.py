from typing import Optional
from pydantic import BaseModel, Field


class Config(BaseModel):
    naver_commission: float = Field(default=3.5, description="네이버 수수료 (%)")
    coupang_commission: float = Field(default=5.0, description="쿠팡 수수료 (%)")
    shipping_cost: float = Field(default=3000, description="배송비 (원)")
    other_cost: float = Field(default=0, description="기타비용 (원)")
    target_margin: float = Field(default=20.0, description="목표 마진율 (%)")
    tax_rate: float = Field(default=0.0, description="부가세율 (%) - 0이면 미적용")


class ReturnChecklist(BaseModel):
    refund_complete: bool = Field(default=False, description="환불 완료")
    customer_contact: bool = Field(default=False, description="고객 연락")
    stock_updated: bool = Field(default=False, description="재고 반영")
    shipping_fee_handled: bool = Field(default=False, description="배송비 처리")
    tax_invoice_issued: bool = Field(default=False, description="세금계산서 발행")


class ReturnUpdate(BaseModel):
    return_occurred: bool = Field(default=False, description="반품 발생 여부")
    return_checklist: ReturnChecklist = Field(default_factory=ReturnChecklist, description="반품 체크리스트")


class ItemCreate(BaseModel):
    name: str = Field(..., description="상품명")
    purchase_price: float = Field(..., ge=0, description="매입가 (원)")
    naver_price: Optional[float] = Field(default=None, ge=0, description="네이버 판매가 (원)")
    coupang_price: Optional[float] = Field(default=None, ge=0, description="쿠팡 판매가 (원)")
    source_type: Optional[str] = Field(default="해외", description="소싱처 종류 (해외/국내)")
    source: Optional[str] = Field(default="", description="소싱처 이름")
    url: Optional[str] = Field(default="", description="소싱 URL")
    wholesale_price: Optional[float] = Field(default=None, ge=0, description="최저가/도매가 (원)")
    min_order_qty: Optional[int] = Field(default=None, ge=1, description="최소주문수량")
    has_customs_tax: bool = Field(default=False, description="관부가세 유무")
    memo: Optional[str] = Field(default="", description="메모")
    return_occurred: bool = Field(default=False, description="반품 발생 여부")
    return_checklist: ReturnChecklist = Field(default_factory=ReturnChecklist, description="반품 체크리스트")


class Item(ItemCreate):
    id: int
