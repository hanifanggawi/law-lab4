from fastapi import UploadFile
from sqlalchemy.orm import Session

from . import models, schemas

def get_products(db: Session):
    return db.query(models.Product).all()

def get_products_by_id(db: Session, id: int):
    return db.query(models.Product).filter(models.Product.id == id).first()

def get_products_by_filters(db: Session, filters):
    return db.query(models.Product).filter_by(**filters).all()

def create_product(db: Session, product: schemas.ProductCreate):
    db_product = models.Product(**product.dict())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product

def update_product(db: Session, product: schemas.ProductCreate, db_product=models.Product):
    db_product.name = product.name
    db_product.brand = product.brand
    db_product.price = product.price
    db.commit()
    return db_product

def delete_product(db: Session, product: schemas.ProductCreate):
    db.delete(product)
    db.commit()

def create_file(db: Session, file: UploadFile):
    contents = file.file.read()
    db_file = models.File(file=contents, file_name=file.filename)
    db.add(db_file)
    db.commit()
    db.refresh(db_file)
    return db_file