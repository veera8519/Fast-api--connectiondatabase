from fastapi import FastAPI
from product import schema

from database import engine
from product import models

models.Base.metadata.create_all(engine)

app=FastAPI()

@app.post("/product")
def create_product(request:schema.Product):
    return request