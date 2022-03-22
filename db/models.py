from sqlalchemy import Column, Integer, String, LargeBinary

from .database import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer, primary_key=True, index=True)
    brand = Column(String, index=True)
    name = Column(String, index=True)
    price = Column(Integer)

class File(Base):
    __tablename__ = "file"

    id = Column(Integer, primary_key=True, index=True)
    file = Column(LargeBinary)
    file_name = Column(String)