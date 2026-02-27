from typing import Optional

from fastapi.params import Query
from pydantic import BaseModel


class ResponseMessage(BaseModel):
    message: str

class BaseFilter(BaseModel):
    limit: Optional[int] = Query(None)
    offset: Optional[int] = Query(None)