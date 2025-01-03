from pydantic import BaseModel
from sqlalchemy import Integer, String, Column, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

# Pydantic models for serialization (without circular references)
class UserBase(BaseModel):
    user_id: int
    username: str
    email: str
    password:str
class RoleBase(BaseModel):
    user_id: int
    role_name: str
Base = declarative_base()

# SQLAlchemy models with relationships
class UserDB(Base):
    __tablename__ = 'users'
    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, nullable=False, index=True)
    email = Column(String, index=True)
    password = Column(String(1000), nullable=False)
    


class RoleDB(Base):
    __tablename__ = 'roles'
    user_id = Column(Integer, ForeignKey('users.user_id'), primary_key=True)
    role_name = Column(String, nullable=False, default="client")
