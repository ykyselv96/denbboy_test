from pydantic import BaseModel
from typing import List, Optional

class TagBase(BaseModel):
    name: str

class TagCreate(TagBase):
    pass

class TagUpdate(BaseModel):
    name: Optional[str]

class TagDB(TagBase):
    id: int

    class Config:
        orm_mode = True
