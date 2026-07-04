from sqlalchemy import Column, String, ForeignKey, Numeric, Text, JSON, DateTime
from sqlalchemy.orm import relationship
from app.core.models import AuditMixin, Base
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.sql import func

class RepairTicket(AuditMixin, Base):
    __tablename__ = "repair_tickets"
    ticket_number = Column(String(20), unique=True, index=True)
    customer_id = Column(UUID(as_uuid=True), ForeignKey('users.id'))
    technician_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True)
    
    # Device Info
    device_brand = Column(String(50))
    device_model = Column(String(100))
    imei_1 = Column(String(50), nullable=True)
    serial_number = Column(String(50), nullable=True)
    
    # Security (Encrypted in production)
    passcode = Column(String(50), nullable=True)
    pattern_lock = Column(JSONB, nullable=True) 
    
    # Workflow
    status = Column(String(50), default="RECEIVED") # RECEIVED, DIAGNOSING, WAITING_PARTS...
    priority = Column(String(20), default="NORMAL")
    estimated_cost = Column(Numeric(10, 2), nullable=True)
    estimated_delivery = Column(DateTime(timezone=True), nullable=True)
    
    # Checklists & Accessories (Stored as JSONB for flexibility)
    accessories_received = Column(JSONB, default=list) # e.g., ["SIM", "Case"]
    pre_repair_checklist = Column(JSONB, default=dict) # e.g., {"FaceID": "Working", "WaterDamage": "Yes"}
    
    # Relationships
    timeline = relationship("RepairTimeline", back_populates="ticket", cascade="all, delete-orphan")
    parts_used = relationship("RepairPart", back_populates="ticket")

class RepairTimeline(AuditMixin, Base):
    __tablename__ = "repair_timeline"
    ticket_id = Column(UUID(as_uuid=True), ForeignKey('repair_tickets.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), nullable=True) # Who made the change
    action = Column(String(100)) # e.g., "STATUS_CHANGED", "NOTE_ADDED", "CUSTOMER_SMS_SENT"
    details = Column(Text, nullable=True)
    
    ticket = relationship("RepairTicket", back_populates="timeline")

class RepairPart(AuditMixin, Base):
    __tablename__ = "repair_parts"
    ticket_id = Column(UUID(as_uuid=True), ForeignKey('repair_tickets.id'))
    product_id = Column(UUID(as_uuid=True), ForeignKey('inventory.id'))
    quantity = Column(Numeric(10, 2), default=1)
    cost_price = Column(Numeric(10, 2))
    selling_price = Column(Numeric(10, 2))
    
    ticket = relationship("RepairTicket", back_populates="parts_used")
