from typing import List
from fastapi import Depends, HTTPException, status
from schemas.author_schema import AuthorCreate, AuthorDB, AuthorUpdate
from core.get_db_session import get_session
from models.models import Author
from sqlalchemy import select, or_, delete, update



class AuthorCrud:
    def __init__(self, db):
        self.db = db

    async def if_author_in_db(self, author_name: str, author_email: str):
        statement = select(Author).where(or_(
            Author.name == author_name,
            Author.email == author_email
        ))
        result = await self.db.execute(statement=statement)
        author_in_db = result.scalars().first()

        if author_in_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='There is already another author with this name or email',
            )

    async def create_author(self, payload: AuthorCreate) -> AuthorDB:
        await self.if_author_in_db(author_name=payload.name, author_email=payload.email)

        db_author = Author(name=payload.name, email=payload.email)

        self.db.add(db_author)
        await self.db.commit()
        await self.db.refresh(db_author)
        return db_author

    async def get_all_authors(self) -> List[AuthorDB]:
        db_result = await self.db.execute(select(Author))
        return db_result.scalars().all()

    async def get_author_by_id(self, author_id: int) -> AuthorDB:

        statement = select(Author).where(Author.id == author_id)
        result = await self.db.execute(statement=statement)
        author_in_db = result.scalars().first()

        if not author_in_db:
            raise HTTPException(status_code=404, detail="Author_not_found")

        return author_in_db


    async def update_author(self, author_id: int, payload: AuthorUpdate) -> AuthorDB:

        await self.if_author_in_db(author_name=payload.name, author_email=payload.email)
        author_in_db = await self.get_author_by_id(author_id=author_id)

        if author_in_db:
            values_to_update = {}

            if payload.name:
                values_to_update['name'] = payload.name

            if payload.email:
                values_to_update['email'] = payload.email

            statement = update(Author).where(Author.id == author_id).values(**values_to_update)

            await self.db.execute(statement)
            await self.db.commit()
            res_in_db = await self.get_author_by_id(author_id)

        return res_in_db








    async def delete_author(self, author_id: int) -> AuthorDB:

        author_in_db = await self.get_author_by_id(author_id=author_id)

        statement = delete(Author).where(Author.id == author_id)
        await self.db.execute(statement=statement)
        await self.db.commit()
        return author_in_db


def get_author_crud(db=Depends(get_session)) -> AuthorCrud:
    return AuthorCrud(db=db)
