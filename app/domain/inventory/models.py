from sqlalchemy import Column, String, ForeignKey, Numeric, Integer, Boolean, Text
from sqlalchemy.orm import relationship
from app.core.models import AuditMixin, Base
from sqlalchemy.dialects.postgresql import UUID

class Category(AuditMixin, Base):
    __tablename__ = "categories"
    name = Column(String(100), unique=True, index=True) # e.g., Phones, Displays, Batteries
    is_serialized = Column(Boolean, default=False)

class Product(AuditMixin, Base):
    __tablename__ = "products"
    sku = Column(String(50), unique=True, index=True)
    barcode = Column(String(100), unique=True, index=True, nullable=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey('categories.id'))
    supplier_id = Column(UUID(as_uuid=True), ForeignKey('suppliers.id'), nullable=True)
    
    brand = Column(String(50), index=True)
    model_name = Column(String(100), index=True)
    description = Column(Text, nullable=True)
    
    # Pricing
    purchase_price = Column(Numeric(10, 2), nullable=False)
    selling_price = Column(Numeric(10, 2), nullable=False)
    gst_rate = Column(Numeric(5, 2), default=0.00)
    
    # Stock Levels
    stock_available = Column(Integer, default=0)
    stock_reserved = Column(Integer, default=0)
    min_stock = Column(Integer, default=5)
    max_stock = Column(Integer, default=50)
    
    location_bin = Column(String(50), nullable=True) # e.g., "Aisle 3, Shelf B"
    has_warranty = Column(Boolean, default=True)
    
    category = relationship("Category")
    serials = relationship("SerialNumber", back_populates="product")
    movements = relationship("StockMovement", back_populates="product")

class SerialNumber(AuditMixin, Base):
    """Tracks individual units for phones or high-value parts."""
    __tablename__ = "serial_numbers"
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'))
    serial_or_imei = Column(String(100), unique=True, index=True)
    status = Column(String(20), default="IN_STOCK") # IN_STOCK, RESERVED, SOLD, RETURNED
    
    product = relationship("Product", back_populates="serials")

class StockMovement(AuditMixin, Base):
    """Immutable ledger of all stock changes."""
    __tablename__ = "stock_movements"
    product_id = Column(UUID(as_uuid=True), ForeignKey('products.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id')) # Who moved it
    change_amount = Column(Integer, nullable=False) # Positive or Negative
    movement_type = Column(String(50)) # PURCHASE, SALE, REPAIR_USE, MANUAL_ADJUSTMENT, RETURN
    reference_id = Column(UUID(as_uuid=True), nullable=True) # Links to Order ID or Repair ID
    notes = Column(Text, nullable=True)
    
    product = relationship("Product", back_populates="movements")
