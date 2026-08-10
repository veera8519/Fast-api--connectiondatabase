from warnings import deprecated

from fastapi import Depends, FastAPI,HTTPException,status
from sqlalchemy import inspect, text
from sqlalchemy.orm import Session

from database import engine, SessionLocal
from product import models, schema


from passlib.context import CryptContext

models.Base.metadata.create_all(bind=engine)



app = FastAPI()


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

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
        price=request.price,
        seller_id=1
    )

    db.add(new_product)
    db.commit()
    db.refresh(new_product)

    return new_product


@app.get('/product')
def all_products(db:Session=Depends(get_db)):
    products=db.query(models.Product).all()
    return products

@app.get('/product/{id}',response_model=schema.ShowProduct)
def product_id(id:int,db:Session=Depends(get_db)):
    product=db.query(models.Product).filter(models.Product.id==id).first()
    if not product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail='NOT FOUND')
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

#Route from Seels 
@app.post('/sellers',response_model=schema.DisplaySeller)
def create_post_seller(request:schema.Sellers,db:Session=Depends(get_db)):
    hashedpassword=pwd_context.hash(request.password)
    new_seller=models.Seller(username=request.username,email=request.email,password=hashedpassword)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller


