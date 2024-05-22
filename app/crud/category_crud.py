from typing import List
from fastapi import Depends, HTTPException, status
from schemas.categories_schema import CategoryCreate, CategoryDB, CategoryBase, CategoryUpdate
from core.get_db_session import get_session
from models.models import Category
from sqlalchemy import select, or_, delete, update



class CategoryCrud:
    def __init__(self, db):
        self.db = db

    async def if_category_in_db(self, category_name: str):
        statement = select(Category).where(
            Category.name == category_name,
        )
        result = await self.db.execute(statement=statement)
        category_in_db = result.scalars().first()

        if category_in_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='This category is already exists',
            )

    async def create_category(self, payload: CategoryCreate) -> CategoryDB:
        await self.if_category_in_db(category_name=payload.name)

        db_category = Category(name=payload.name)

        self.db.add(db_category)
        await self.db.commit()
        await self.db.refresh(db_category)
        return db_category

    async def get_all_categories(self) -> List[CategoryDB]:
        db_result = await self.db.execute(select(Category))
        return db_result.scalars().all()


    async def get_category_by_id(self, category_id: int) -> CategoryDB:

        statement = select(Category).where(Category.id == category_id)
        result = await self.db.execute(statement=statement)
        category_in_db = result.scalars().first()

        if not category_in_db:
            raise HTTPException(status_code=404, detail="Category_not_found")

        return category_in_db


    async def update_category(self, category_id: int, payload: CategoryUpdate) -> CategoryDB:

        await self.if_category_in_db(category_name=payload.name)

        category_in_db = await self.get_category_by_id(category_id=category_id)

        statement = update(Category).where(Category.id == category_id).values(name=payload.name)

        await self.db.execute(statement)
        await self.db.commit()
        res_in_db = await self.get_category_by_id(category_id=category_id)

        return res_in_db


    async def delete_category(self, category_id: int) -> CategoryDB:

        category_in_db = await self.get_category_by_id(category_id=category_id)

        statement = delete(Category).where(Category.id == category_id)
        await self.db.execute(statement=statement)
        await self.db.commit()
        return category_in_db


def get_category_crud(db=Depends(get_session)) -> CategoryCrud:
    return CategoryCrud(db=db)
