from sqlalchemy import Column, String, ForeignKey, Boolean, JSON, Text
from sqlalchemy.orm import relationship
from app.core.models import AuditMixin, Base
from sqlalchemy.dialects.postgresql import UUID, JSONB

class AutomationRule(AuditMixin, Base):
    """Defines what happens when a specific event occurs."""
    __tablename__ = "automation_rules"
    shop_id = Column(UUID(as_uuid=True), index=True) # For multi-tenant isolation
    
    name = Column(String(100), nullable=False)
    event_trigger = Column(String(50), index=True) # e.g., 'REPAIR_STATUS_CHANGED'
    condition = Column(JSONB, nullable=True) # e.g., {"new_status": "READY"}
    
    action_type = Column(String(50)) # e.g., 'SEND_SMS', 'SEND_EMAIL', 'CREATE_PO'
    action_payload = Column(JSONB) # Template data, recipient logic
    
    is_active = Column(Boolean, default=True)

class TaskLog(AuditMixin, Base):
    """Audit trail for background tasks to ensure accountability."""
    __tablename__ = "task_logs"
    task_id = Column(String(255), unique=True, index=True)
    rule_id = Column(UUID(as_uuid=True), ForeignKey('automation_rules.id'), nullable=True)
    status = Column(String(20)) # PENDING, SUCCESS, FAILED
    error_message = Column(Text, nullable=True)
