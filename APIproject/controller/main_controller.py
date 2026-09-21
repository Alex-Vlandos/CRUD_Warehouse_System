from fastapi import FastAPI,APIRouter
from controller.product_controller import product_router
from controller.orders_controller import order_router

app = FastAPI()

app.include_router(product_router)
app.include_router(order_router)