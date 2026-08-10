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


@app.get('/products')
def all_products(db:Session=Depends(get_db)):
    products=db.query(models.Product).all()
    return products