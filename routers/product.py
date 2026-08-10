from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from database import get_db
from product import models, schema


router = APIRouter(
    prefix="/product",
    tags=["PRODUCTS"]
)


# CREATE PRODUCT
@router.post("/")
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


# GET ALL PRODUCTS
@router.get("/")
def all_products(
    db: Session = Depends(get_db)
):
    products = db.query(models.Product).all()

    return products


# GET PRODUCT BY ID
@router.get("/{id}", response_model=schema.ShowProduct)
def product_id(
    id: int,
    db: Session = Depends(get_db)
):
    product = (
        db.query(models.Product)
        .filter(models.Product.id == id)
        .first()
    )

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    return product


# DELETE PRODUCT
@router.delete("/{id}")
def product_del(
    id: int,
    db: Session = Depends(get_db)
):
    product = (
        db.query(models.Product)
        .filter(models.Product.id == id)
        .delete(synchronize_session=False)
    )

    if product == 0:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    db.commit()

    return {
        "message": "Product deleted successfully"
    }


# UPDATE PRODUCT
@router.put("/{id}")
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
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Product not found"
        )

    product_query.name = request.name
    product_query.description = request.description
    product_query.price = request.price
    product_query.seller_id = request.seller_id

    db.commit()
    db.refresh(product_query)

    return product_query