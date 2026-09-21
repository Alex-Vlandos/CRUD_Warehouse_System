from typing import Optional
from pydantic import BaseModel

class SearchProducts(BaseModel):
    name : Optional[str]=None
    min_price : Optional[float]=None
    max_price : Optional[float]=None
    min_quantity : Optional[int]=None
    max_quantity : Optional[int]=None