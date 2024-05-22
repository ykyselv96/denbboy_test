from typing import List
from fastapi import Depends, HTTPException, status
from schemas.posts_schema import PostCreate, PostDB, PostBase, PostUpdate
from core.get_db_session import get_session
from models.models import Post, Author, Category, Tag, post_author, post_category, post_tag
from sqlalchemy import select, delete, update, insert
from sqlalchemy.orm import joinedload


class PostCrud:

    def __init__(self, db):
        self.db = db

    async def if_post_in_db(self, post_title: str):

        statement = select(Post).where(
            Post.title == post_title,
        )
        result = await self.db.execute(statement=statement)
        post_in_db = result.scalars().first()

        if post_in_db:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='This post is already exists',
            )

    async def create_post(self, payload: PostCreate) -> PostDB:

        await self.if_post_in_db(post_title=payload.title)
        db_post = Post(title=payload.title, content=payload.content)
        self.db.add(db_post)
        await self.db.flush()

        for author_id in payload.author_ids:
            statement = select(Author).where(Author.id == author_id)
            result = await self.db.execute(statement=statement)
            author = result.scalars().first()
            if author:
                statement = insert(post_author).values(post_id=db_post.id, author_id=author.id)
                await self.db.execute(statement)

        for category_id in payload.category_ids:
            statement = select(Category).where(Category.id == category_id)
            result = await self.db.execute(statement=statement)
            category = result.scalars().first()
            if category:
                statement = insert(post_category).values(post_id=db_post.id, category_id=category.id)
                await self.db.execute(statement)

        for tag_id in payload.tag_ids:
            statement = select(Tag).where(Tag.id == tag_id)
            result = await self.db.execute(statement=statement)
            tag = result.scalars().first()
            if tag:
                statement = insert(post_tag).values(post_id=db_post.id, tag_id=tag.id)
                await self.db.execute(statement)

        await self.db.commit()
        await self.db.refresh(db_post)
        post_in_db = await self.get_post_by_id(db_post.id)
        return post_in_db

    async def get_all_posts(self) -> List[PostDB]:
        statement = select(Post).options(joinedload(Post.authors),joinedload(Post.categories),
            joinedload(Post.tags))
        result = await self.db.execute(statement)
        post = result.unique().scalars().all()
        return post

    async def get_post_by_id(self, post_id: int) -> PostDB:
        statement = select(Post).options(
            joinedload(Post.authors),
            joinedload(Post.categories),
            joinedload(Post.tags)
        ).where(Post.id == post_id)
        result = await self.db.execute(statement)
        post = result.unique().scalars().first()
        if not post:
            raise HTTPException(status_code=404, detail="Post_not_found")

        return post

    async def update_post(self, post_id: int, payload: PostUpdate) -> PostDB:

        statement_gen = update(Post).where(Post.id == post_id)

        if payload.title:
            statement_gen = statement_gen.values(title=payload.title)
            print(payload.title)
        if payload.content:
            statement_gen = statement_gen.values(content=payload.content)

        await self.db.execute(statement_gen)

        if payload.author_ids:
            await self.db.execute(delete(post_author).where(post_author.c.post_id == post_id))
            for author_id in payload.author_ids:
                statement = select(Author).where(Author.id == author_id)
                result = await self.db.execute(statement)
                author = result.scalars().first()
                if author:
                    statement = insert(post_author).values(post_id=post_id, author_id=author.id)
                    await self.db.execute(statement)

        if payload.category_ids:
            await self.db.execute(delete(post_category).where(post_category.c.post_id == post_id))
            for category_id in payload.category_ids:
                statement = select(Category).where(Category.id == category_id)
                result = await self.db.execute(statement)
                category = result.scalars().first()
                if category:
                    statement = insert(post_category).values(post_id=post_id, category_id=category.id)
                    await self.db.execute(statement)

        if payload.tag_ids:
            await self.db.execute(delete(post_tag).where(post_tag.c.post_id == post_id))
            for tag_id in payload.tag_ids:
                statement = select(Tag).where(Tag.id == tag_id)
                result = await self.db.execute(statement)
                tag = result.scalars().first()
                if tag:
                    statement = insert(post_tag).values(post_id=post_id, tag_id=tag.id)
                    await self.db.execute(statement)

        await self.db.commit()
        statement = select(Post).options(
            joinedload(Post.authors),
            joinedload(Post.categories),
            joinedload(Post.tags)
        ).where(Post.id == post_id)
        result = await self.db.execute(statement)
        db_post = result.unique().scalars().first()
        return db_post


    async def delete_post(self, post_id: int) -> PostDB:
        post_in_db = await self.get_post_by_id(post_id=post_id)
        await self.db.execute(delete(post_author).where(post_author.c.post_id == post_id))
        await self.db.execute(delete(post_category).where(post_category.c.post_id == post_id))
        await self.db.execute(delete(post_tag).where(post_tag.c.post_id == post_id))
        await self.db.execute(delete(Post).where(Post.id == post_id))
        await self.db.commit()
        return post_in_db

def get_post_crud(db=Depends(get_session)) -> PostCrud:
    return PostCrud(db=db)
