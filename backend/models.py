from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from .database import Base

class Product(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    code = Column(String(64), unique=True, index=True, nullable=False)
    name = Column(String(255), nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)

class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, server_default=func.now(), nullable=False)
    subtotal = Column(Numeric(12, 2), nullable=False)
    tax = Column(Numeric(12, 2), nullable=False)
    total = Column(Numeric(12, 2), nullable=False)
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")

class OrderItem(Base):
    __tablename__ = "order_items"
    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id"), nullable=False)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    unit_price = Column(Numeric(12, 2), nullable=False)
    order = relationship("Order", back_populates="items") 