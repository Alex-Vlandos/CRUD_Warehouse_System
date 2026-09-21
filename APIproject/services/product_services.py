from typing import List,Optional
from domain.product import Product
from repository.database import create_product_db,update_product_db,delete_product_db

def create_products(products : List[Product]):
    for product in products:
        create_product_db(product.name,product.desc,product.price,product.quantity)
    return {f"message" : f"{len(products)} products created!","products" : products}

def update_product(product:Product,product_id):
    update_product_db(product_id,product.name,product.desc,product.price,product.quantity)
    return {f"message " : {f"Product with id : {product_id} changed, new name : {product.name},new desc : {product.desc},new price : {product.price},"
                           f"new quantity" : {product.quantity}}}

def delete_product(product_id):
    delete_product_db(product_id)
    return {f"message" : f"Product with id : {product_id} has been deleted successfully!"}

