from fastapi import FastAPI

from database import engine
from product import models
from routers import product, seller


# Create database tables
models.Base.metadata.create_all(bind=engine)


# Create FastAPI application
app = FastAPI(
    title="Products API",
    description="THIS IS SHOPPING CART API"
)


# Include routers
app.include_router(product.router)
app.include_router(seller.router)