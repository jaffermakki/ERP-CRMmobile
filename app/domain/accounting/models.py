from sqlalchemy import Column, String, ForeignKey, Numeric, Date, Text
from sqlalchemy.orm import relationship
from app.core.models import AuditMixin, Base
from sqlalchemy.dialects.postgresql import UUID

class ExpenseCategory(AuditMixin, Base):
    __tablename__ = "expense_categories"
    name = Column(String(100), unique=True, index=True) # e.g., Rent, Utilities, Tools, Marketing

class Expense(AuditMixin, Base):
    __tablename__ = "expenses"
    category_id = Column(UUID(as_uuid=True), ForeignKey('expense_categories.id'))
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id')) # Logged by
    
    amount = Column(Numeric(10, 2), nullable=False)
    date_incurred = Column(Date, nullable=False, index=True)
    vendor = Column(String(100), nullable=True)
    receipt_url = Column(String(255), nullable=True)
    notes = Column(Text, nullable=True)
    
    category = relationship("ExpenseCategory")

# Note: The actual Reporting service will heavily utilize SQLAlchemy 'func.sum', 'func.count', 
# and 'extract' methods against the Order, RepairTicket, and Expense tables.
