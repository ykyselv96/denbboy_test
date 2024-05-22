from pydantic import BaseModel
from typing import List, Optional
from .author_schema import AuthorDB
from .categories_schema import CategoryDB
from .tags_schema import TagDB

class PostBase(BaseModel):
    title: str
    content: str

class PostCreate(PostBase):
    author_ids: List[int]
    category_ids: List[int]
    tag_ids: List[int]

class PostUpdate(BaseModel):
    title: Optional[str]
    content: Optional[str]
    author_ids: Optional[List[int]]
    category_ids: Optional[List[int]]
    tag_ids: Optional[List[int]]

class PostDB(PostBase):
    id: int
    authors: List['AuthorDB'] = []
    categories: List[CategoryDB] = []
    tags: List[TagDB] = []

    class Config:
        orm_mode = True
