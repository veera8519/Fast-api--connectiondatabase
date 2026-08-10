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