from sqlalchemy import Column, Integer, String
from database.base import Base

class User(Base):
    __tablename__ = "test_zzy"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)

