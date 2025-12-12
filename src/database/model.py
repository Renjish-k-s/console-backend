from database import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

class Tenant(Base):
    __tablename__ = "tenants"

    tenant_id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)

    users = relationship("User", back_populates="tenant")
    products_link = relationship("TenantProductMapping", back_populates="tenant")
    roles = relationship("Role", back_populates="tenant")


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), unique=True, index=True)
    email = Column(String(150), unique=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id"))

    tenant = relationship("Tenant", back_populates="users")
    user_roles = relationship("RoleUserMapping", back_populates="user")


class Role(Base):
    __tablename__ = "roles"

    role_id = Column(Integer, primary_key=True, index=True)
    role_name = Column(String(50), unique=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id"))

    tenant = relationship("Tenant", back_populates="roles")
    role_users = relationship("RoleUserMapping", back_populates="role")
    app_mappings = relationship("AppRoleMapping", back_populates="role")


class RoleUserMapping(Base):
    __tablename__ = "role_user_mappings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.user_id"))
    role_id = Column(Integer, ForeignKey("roles.role_id"))
    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id"))

    tenant = relationship("Tenant")
    role = relationship("Role", back_populates="role_users")
    user = relationship("User", back_populates="user_roles")


class Product(Base):
    __tablename__ = "products"

    product_id = Column(Integer, primary_key=True, index=True)
    product_name = Column(String(100), index=True)
    launch_url = Column(String(255), index=True)
    sub_mode = Column(Boolean, default=False)
    product_logo = Column(String(255), index=True)
    product_description = Column(String(500), index=True)

    tenant_mappings = relationship("TenantProductMapping", back_populates="product")
    app_roles = relationship("AppRoleMapping", back_populates="product")


class TenantProductMapping(Base):
    __tablename__ = "tenant_product_mappings"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id"))
    product_id = Column(Integer, ForeignKey("products.product_id"))

    tenant = relationship("Tenant", back_populates="products_link")
    product = relationship("Product", back_populates="tenant_mappings")


class AppRoleMapping(Base):
    __tablename__ = "app_role_mappings"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.product_id"))
    role_id = Column(Integer, ForeignKey("roles.role_id"))
    tenant_id = Column(Integer, ForeignKey("tenants.tenant_id"))

    product = relationship("Product", back_populates="app_roles")
    role = relationship("Role", back_populates="app_mappings")
    tenant = relationship("Tenant")
