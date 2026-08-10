from re import S
from typing import Optional

from pydantic  import BaseModel,ConfigDict

class Product(BaseModel):
    name:str
    description:str
    price: int 

class ShowProduct(BaseModel):
    model_config=ConfigDict(from_attributes=True)
    name:str
    price:int

class Sellers(BaseModel):
    username:str
    email:str
    password:str

class DisplaySeller(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    username: str
    email: str

class login(BaseModel):
    user:str
    password:str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    username:Optional[str]=None