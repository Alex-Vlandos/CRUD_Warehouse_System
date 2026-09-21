from typing import Optional
from pydantic import BaseModel

class Product(BaseModel):
    name : Optional[str] = None
    desc : Optional[str] = None
    price : Optional[float] = None
    quantity : Optional[int] = None