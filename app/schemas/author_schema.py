from pydantic import BaseModel
from typing import Optional

class AuthorBase(BaseModel):
    name: str
    email: str

class AuthorCreate(AuthorBase):
    pass

class AuthorUpdate(BaseModel):
    name: Optional[str]
    email: Optional[str]

class AuthorDB(AuthorBase):
    id: int

    class Config:
        orm_mode = True
