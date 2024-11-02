from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.sql import func
from database import Base


class SpimexTradingResult(Base):
    __tablename__ = 'spimex_trading_results'

    id = Column(Integer, primary_key=True, index=True)
    # Основное поле, которое должно быть заполнено
    exchange_product_id = Column(String, nullable=False)
    exchange_product_name = Column(
        String, nullable=True)  # Сделано необязательным
    oil_id = Column(String, nullable=True)  # Сделано необязательным
    delivery_basis_id = Column(String, nullable=True)  # Сделано необязательным
    delivery_basis_name = Column(
        String, nullable=True)  # Сделано необязательным
    delivery_type_id = Column(String, nullable=True)  # Сделано необязательным
    volume = Column(Float, nullable=True)  # Сделано необязательным
    total = Column(Float, nullable=True)  # Сделано необязательным
    count = Column(Integer, nullable=True)  # Сделано необязательным
    date = Column(DateTime, nullable=False,
                  default=func.now())  # Дата обязательна
    created_on = Column(DateTime, server_default=func.now())
    updated_on = Column(DateTime, server_default=func.now(),
                        onupdate=func.now())
