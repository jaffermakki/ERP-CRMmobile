from sqlalchemy import Column, String, ForeignKey, Boolean, Table
from sqlalchemy.orm import relationship
from app.core.models import AuditMixin, Base
from sqlalchemy.dialects.postgresql import UUID

# Many-to-Many association table for Roles and Permissions
role_permissions = Table(
    'role_permissions',
    Base.metadata,
    Column('role_id', UUID(as_uuid=True), ForeignKey('roles.id')),
    Column('permission_id', UUID(as_uuid=True), ForeignKey('permissions.id'))
)

class Role(AuditMixin, Base):
    __tablename__ = "roles"
    name = Column(String(50), unique=True, index=True)
    description = Column(String(255))
    permissions = relationship("Permission", secondary=role_permissions)

class Permission(AuditMixin, Base):
    __tablename__ = "permissions"
    name = Column(String(50), unique=True, index=True) # e.g., 'pos:write', 'reports:read'

class User(AuditMixin, Base):
    __tablename__ = "users"
    email = Column(String(255), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    full_name = Column(String(100))
    role_id = Column(UUID(as_uuid=True), ForeignKey('roles.id'))
    role = relationship("Role")
