
from fastapi import APIRouter

from fastapi import APIRouter,status,HTTPException

from product import schema

from sqlalchemy.orm import Session

from fastapi.params import Depends

from database  import get_db

from product import models

router=APIRouter(
    tags=['Seller']
)

from passlib.context import CryptContext


pwd_context = CryptContext(
    schemes=["bcrypt"],
    deprecated="auto"
)

@router.post('/sellers',response_model=schema.DisplaySeller)
def create_post_seller(request:schema.Sellers,db:Session=Depends(get_db)):
    hashedpassword=pwd_context.hash(request.password)
    new_seller=models.Seller(username=request.username,email=request.email,password=hashedpassword)
    db.add(new_seller)
    db.commit()
    db.refresh(new_seller)
    return new_seller

