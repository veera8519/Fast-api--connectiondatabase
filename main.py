from fastapi import Depends, FastAPI
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from product import models, schema


models.Base.metadata.create_all(bind=engine)



app = FastAPI()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post("/product")
def create_product(
    request: schema.Product,
    db: Session = Depends(get_db)
):
    new_product = models.Product(
        name=request.name,
        description=request.description,
        price=request.price
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@app.get('/product')
def all_products(db:Session=Depends(get_db)):
    products=db.query(models.Product).all()
    return products

@app.get('/product/{id}')
def product_id(id:int,db:Session=Depends(get_db)):
    product=db.query(models.Product).filter(models.Product.id==id).first()
    return product

@app.delete('/product/{id}')
def product_del(id:int,db:Session=Depends(get_db)):
    product=db.query(models.Product).filter(models.Product.id==id).delete(synchronize_session=False)
    db.commit()
    return product

@app.put("/product/{id}")
def update_product(
    id: int,
    request: schema.Product,
    db: Session = Depends(get_db)
):
    product_query = (
        db.query(models.Product)
        .filter(models.Product.id == id)
        .first()
    )

    if product_query is None:
        return {"message": "Product not found"}

    product_query.name = request.name
    product_query.description = request.description
    product_query.price = request.price

    db.commit()
    db.refresh(product_query)

    return product_query