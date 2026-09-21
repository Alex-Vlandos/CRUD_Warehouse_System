from fastapi import FastAPI,APIRouter
from typing import List
from services.product_services import *
from domain.product import Product
from domain.search_products import SearchProducts
from repository.database import get_products_details_db,search_products_db

product_router = APIRouter()

@product_router.post("/create-products")
async def create_products_api(products : List[Product]):
    return create_products(products)

@product_router.get("/read-products")
async def read_products_api():
    return get_products_details_db()

@product_router.patch("/update-product/{product_id}")
async def update_product_api(product_id:int,product:Product):
    return update_product(product,product_id)

@product_router.delete("/delete-product/{product_id}")
async def delete_product_api(product_id:int):
    return delete_product(product_id)

@product_router.post("/search-products")
async def search_products_api(criteria : SearchProducts):
    return search_products_db(criteria.name,criteria.min_price,criteria.max_price,criteria.min_quantity,criteria.max_quantity)