from fastapi import APIRouter
from services.order_services import place_order,update_order,delete_order
from domain.order import Order
from repository.database import products_statistics_db

order_router = APIRouter()

@order_router.post("/place-order")
async def place_order_api(order : Order):
   return place_order(order)

@order_router.post("/update-order/{order_id}")
async def update_order_api(order_id : int,order : Order):
   return update_order(order_id,order)

@order_router.delete("/delete-order/{order_id}")
async def delete_order_api(order_id : int):
   return delete_order(order_id)

@order_router.get("/products-statistics")
async def statistics_of_products_api():
   return products_statistics_db()