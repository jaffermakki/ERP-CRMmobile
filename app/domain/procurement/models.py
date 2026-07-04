class Supplier(AuditMixin, Base):
    __tablename__ = "suppliers"
    company_name = Column(String(100), index=True)
    contact_name = Column(String(100))
    email = Column(String(100))
    phone = Column(String(20))
    
    # Performance & Financials
    lead_time_days = Column(Integer, default=3)
    outstanding_balance = Column(Numeric(10, 2), default=0.00)
    rating = Column(Numeric(3, 2), default=5.00) # 1 to 5 stars
    
    purchase_orders = relationship("PurchaseOrder", back_populates="supplier")

class PurchaseOrder(AuditMixin, Base):
    __tablename__ = "purchase_orders"
    po_number = Column(String(20), unique=True, index=True)
    supplier_id = Column(UUID(as_uuid=True), ForeignKey('suppliers.id'))
    status = Column(String(20), default="DRAFT") # DRAFT, SENT, PARTIAL, RECEIVED, CANCELLED
    
    total_amount = Column(Numeric(10, 2), default=0.00)
    expected_date = Column(DateTime(timezone=True), nullable=True)
    
    items = relationship("POItem", back_populates="po", cascade="all, delete-orphan")
    supplier = relationship("Supplier", back_populates="purchase_orders")
