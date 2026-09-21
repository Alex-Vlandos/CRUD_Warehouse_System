from pydantic import BaseModel
from typing import List, Optional


class OrderItem(BaseModel):
    product_id : Optional[int]=None
    quantity : Optional[int]=None

class Order(BaseModel):
    customer_name : Optional[str]=None
    products_details : Optional[List[OrderItem]]=None


