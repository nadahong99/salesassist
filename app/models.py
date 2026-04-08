from typing import Optional
from pydantic import BaseModel, Field


class Config(BaseModel):
    naver_commission: float = Field(default=3.5, description="네이버 수수료 (%)")
    coupang_commission: float = Field(default=5.0, description="쿠팡 수수료 (%)")
    shipping_cost: float = Field(default=3000, description="배송비 (원)")
    other_cost: float = Field(default=0, description="기타비용 (원)")
    target_margin: float = Field(default=20.0, description="목표 마진율 (%)")
    tax_rate: float = Field(default=0.0, description="부가세율 (%) - 0이면 미적용")


class OrderCreate(BaseModel):
    order_number: str = Field(..., description="주문번호")
    customer_name: str = Field(..., description="고객명")
    customer_phone: str = Field(default="", description="연락처")
    customer_address: str = Field(default="", description="배송 주소")
    product_name: str = Field(default="", description="상품명")
    quantity: int = Field(default=1, ge=1, description="수량")
    amount: float = Field(default=0, ge=0, description="결제금액 (원)")
    payment_status: str = Field(default="미결제", description="결제 상태")
    delivery_status: str = Field(default="주문접수", description="배송 상태")
    order_date: str = Field(default="", description="주문일")
    memo: str = Field(default="", description="메모")


class Order(OrderCreate):
    id: int


class ReturnChecklist(BaseModel):
    refund_complete: bool = Field(default=False, description="환불 완료")
    customer_contact: bool = Field(default=False, description="고객 연락")
    stock_updated: bool = Field(default=False, description="재고 반영")
    shipping_fee_handled: bool = Field(default=False, description="배송비 처리")


class ReturnUpdate(BaseModel):
    return_occurred: bool = Field(default=False, description="반품 발생 여부")
    return_checklist: ReturnChecklist = Field(default_factory=ReturnChecklist, description="반품 체크리스트")


class ItemCreate(BaseModel):
    name: str = Field(..., description="상품명")
    purchase_price: float = Field(..., ge=0, description="매입가 (원)")
    naver_price: Optional[float] = Field(default=None, ge=0, description="네이버 판매가 (원)")
    coupang_price: Optional[float] = Field(default=None, ge=0, description="쿠팡 판매가 (원)")
    source: Optional[str] = Field(default="", description="소싱처")
    url: Optional[str] = Field(default="", description="소싱 URL")
    memo: Optional[str] = Field(default="", description="메모")
    return_occurred: bool = Field(default=False, description="반품 발생 여부")
    return_checklist: ReturnChecklist = Field(default_factory=ReturnChecklist, description="반품 체크리스트")


class Item(ItemCreate):
    id: int
