from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base


class SpimexTradingResult(Base):
    __tablename__ = 'spimex_trading_results'

    id = Column(Integer, primary_key=True, index=True)
    exchange_product_id = Column(String, nullable=False)
    exchange_product_name = Column(String, nullable=False)
    # First 4 characters of exchange_product_id
    oil_id = Column(String, nullable=False)
    # Characters 4 to 7 of exchange_product_id
    delivery_basis_id = Column(String, nullable=False)
    delivery_basis_name = Column(String, nullable=False)
    # Last character of exchange_product_id
    delivery_type_id = Column(String, nullable=False)
    volume = Column(Float, nullable=False)
    total = Column(Float, nullable=False)
    count = Column(Integer, nullable=False)
    date = Column(DateTime, nullable=False, default=func.now())
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, server_default=func.now(),
                        onupdate=func.now())
