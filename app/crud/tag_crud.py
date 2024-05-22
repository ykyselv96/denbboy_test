from typing import List
from fastapi import Depends, HTTPException, status
from schemas.tags_schema import TagDB, TagCreate, TagBase, TagUpdate
from core.get_db_session import get_session
from models.models import Tag
from sqlalchemy import select, delete, update



class TagCrud:

    def __init__(self, db):
        self.db = db

    async def if_tag_in_db(self, tag_name: str):
        statement = select(Tag).where(
            Tag.name == tag_name,
        )
        result = await self.db.execute(statement=statement)
        tag_in_db = result.scalars().first()

        if tag_in_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='This tag is already exists',
            )

    async def create_tag(self, payload: TagCreate) -> TagDB:
        await self.if_tag_in_db(tag_name=payload.name)

        db_tag = Tag(name=payload.name)

        self.db.add(db_tag)
        await self.db.commit()
        await self.db.refresh(db_tag)
        return db_tag

    async def get_all_tags(self) -> List[TagDB]:
        db_result = await self.db.execute(select(Tag))
        return db_result.scalars().all()

    async def get_tag_by_id(self, tag_id: int) -> TagDB:

        statement = select(Tag).where(Tag.id == tag_id)
        result = await self.db.execute(statement=statement)
        tag_in_db = result.scalars().first()

        if not tag_in_db:
            raise HTTPException(status_code=404, detail="Tag_not_found")

        return tag_in_db

    async def update_tag(self, tag_id: int, payload: TagUpdate) -> TagDB:

        await self.if_tag_in_db(tag_name=payload.name)
        tag_in_db = await self.get_tag_by_id(tag_id=tag_id)

        statement = update(Tag).where(Tag.id == tag_id).values(name=payload.name)

        await self.db.execute(statement)
        await self.db.commit()
        res_in_db = await self.get_tag_by_id(tag_id=tag_id)

        return res_in_db


    async def delete_tag(self, tag_id: int) -> TagDB:

        tag_in_db = await self.get_tag_by_id(tag_id=tag_id)

        statement = delete(Tag).where(Tag.id == tag_id)
        await self.db.execute(statement=statement)
        await self.db.commit()
        return tag_in_db


def get_tag_crud(db=Depends(get_session)) -> TagCrud:
    return TagCrud(db=db)
