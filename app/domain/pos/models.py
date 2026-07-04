from sqlalchemy import Column, String, ForeignKey, Numeric, Integer, Text
from sqlalchemy.orm import relationship
from app.core.models import AuditMixin, Base
from sqlalchemy.dialects.postgresql import UUID

class Order(AuditMixin, Base):
    __tablename__ = "orders"
    customer_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    subtotal = Column(Numeric(10, 2), nullable=False)
    tax_total = Column(Numeric(10, 2), default=0.00)
    discount_total = Column(Numeric(10, 2), default=0.00)
    grand_total = Column(Numeric(10, 2), nullable=False)
    status = Column(String(50), default="COMPLETED") # COMPLETED, REFUNDED, PARTIAL
    notes = Column(Text, nullable=True)
    
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan")

class OrderItem(AuditMixin, Base):
    __tablename__ = "order_items"
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'))
    product_id = Column(UUID(as_uuid=True), ForeignKey('inventory.id')) # Link to inventory phase
    quantity = Column(Integer, nullable=False, default=1)
    unit_price = Column(Numeric(10, 2), nullable=False)
    line_total = Column(Numeric(10, 2), nullable=False)
    imei_serial = Column(String(100), nullable=True)
    
    order = relationship("Order", back_populates="items")

class Payment(AuditMixin, Base):
    __tablename__ = "payments"
    order_id = Column(UUID(as_uuid=True), ForeignKey('orders.id'))
    method = Column(String(50), nullable=False) # CASH, CARD, UPI, STORE_CREDIT
    amount = Column(Numeric(10, 2), nullable=False)
    transaction_ref = Column(String(255), nullable=True)
    
    order = relationship("Order", back_populates="payments")
