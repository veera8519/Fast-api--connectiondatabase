from re import S

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
    username:str
    password:str