from sqlalchemy import Column, Integer, Date, TIMESTAMP, text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Report(Base):
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    report_at = Column(Date, nullable=False)
    order_id = Column(Integer, nullable=False)
    count_product = Column(Integer, nullable=False)
    created_at = Column(TIMESTAMP, server_default=text("NOW()"))