from pydantic import BaseModel, Field
from typing import List

class ProductOut(BaseModel):
    code: str
    name: str
    unit_price: float

class OrderItemIn(BaseModel):
    productCode: str = Field(..., alias="productCode")
    quantity: int

class OrderIn(BaseModel):
    items: List[OrderItemIn]

class OrderOut(BaseModel):
    subtotal: float
    tax: float
    total: float 