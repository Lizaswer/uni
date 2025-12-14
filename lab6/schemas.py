# schemas.py
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    price: float
    quantity: int
    category: Optional[str] = "other"

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemResponse(OrderItemBase):
    id: int
    price: float
    order_id: int
    
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    customer_name: str

class OrderCreate(OrderBase):
    items: List[OrderItemCreate]

class OrderResponse(OrderBase):
    id: int
    total_amount: float
    status: str
    created_at: datetime
    items: List[OrderItemResponse]
    
    class Config:
        from_attributes = True