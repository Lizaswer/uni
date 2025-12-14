from pydantic import BaseModel
from datetime import date, datetime

class ReportCreate(BaseModel):
    report_at: date
    order_id: int
    count_product: int

class ReportResponse(ReportCreate):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True