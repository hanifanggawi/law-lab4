from typing import Optional

from pydantic import BaseModel

class ProductBase(BaseModel):
    name: str
    brand: Optional[str] = None
    price: int

class ProductCreate(ProductBase):
    pass

class Product(ProductBase):
    id: int

    class Config:
        orm_mode = True

class File(BaseModel):
    id: int
    file: bytes
    file_name: str

    class Config:
        orm_mode = True