from sqlalchemy import Column, String, ForeignKey, Numeric, Integer, Text
from sqlalchemy.orm import relationship
from app.core.models import AuditMixin, Base
from sqlalchemy.dialects.postgresql import UUID, JSONB

class Customer(AuditMixin, Base):
    __tablename__ = "customers"
    first_name = Column(String(50), nullable=False)
    last_name = Column(String(50), nullable=False)
    phone = Column(String(20), unique=True, index=True)
    email = Column(String(100), unique=True, index=True, nullable=True)
    
    # Financial & Loyalty
    lifetime_value = Column(Numeric(10, 2), default=0.00)
    outstanding_balance = Column(Numeric(10, 2), default=0.00)
    loyalty_points = Column(Integer, default=0)
    
    # Derived Insights (Updated via background workers)
    favorite_brand = Column(String(50), nullable=True)
    notes = Column(Text, nullable=True)
    
    # Relationships
    orders = relationship("Order", back_populates="customer")
    repairs = relationship("RepairTicket", back_populates="customer")
    communications = relationship("CommunicationLog", back_populates="customer")

class CommunicationLog(AuditMixin, Base):
    __tablename__ = "communication_logs"
    customer_id = Column(UUID(as_uuid=True), ForeignKey('customers.id'))
    type = Column(String(20)) # SMS, EMAIL, WHATSAPP, CALL
    direction = Column(String(10)) # INBOUND, OUTBOUND
    content = Column(Text)
    status = Column(String(20)) # SENT, DELIVERED, FAILED
    
    customer = relationship("Customer", back_populates="communications")
