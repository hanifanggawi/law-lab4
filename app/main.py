from fastapi import Depends, FastAPI, HTTPException, Request, UploadFile
from sqlalchemy.orm import Session

from typing import Optional

from . import crud, models, schemas
from .database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/products/", response_model=schemas.Product)
def create_product(product: schemas.ProductCreate, db: Session = Depends(get_db)):
    return crud.create_product(db=db, product=product)

@app.get("/products/", response_model=list[schemas.Product])
def read_products(req : Request, db: Session = Depends(get_db), name: Optional[str] = None, brand: Optional[str] = None,):
    filters = dict(req.query_params)
    if filters:
        products = crud.get_products_by_filters(db, filters)
    else:
        products = crud.get_products(db)
    if not products:
        raise HTTPException(404, 'No Products found')
    return products

@app.put("/products/{product_id}", response_model=schemas.Product)
def update_product(product: schemas.ProductCreate, product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_products_by_id(db, id = product_id)
    if not db_product:
        raise HTTPException(404, 'Product not found')
    crud.update_product(db=db, product=product, db_product=db_product)
    return db_product

@app.delete("/products/{product_id}")
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = crud.get_products_by_id(db, id = product_id)
    if not db_product:
        raise HTTPException(404, 'Product not found')
    crud.delete_product(db=db, product=db_product)
    return { 'detail' : 'Product successfully deleted'}

@app.post("/uploadfile/")
async def upload_file(file: UploadFile, db: Session = Depends(get_db)):
    try:
        db_file = crud.create_file(db, file=file)
    except:
        raise HTTPException(500, 'Upload Failed')
    return {"detail": f'successfully uploaded {db_file.file_name}'} 