from sqlalchemy import Column, DateTime, Boolean
from sqlalchemy.sql import func
import uuid
from sqlalchemy.dialects.postgresql import UUID

class AuditMixin:
    """Provides standard tracking fields for all commercial entities."""
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True, index=True)
