from fastapi import APIRouter, Depends, status
from schemas.author_schema import AuthorCreate, AuthorDB, AuthorUpdate
from crud.author_crud import AuthorCrud, get_author_crud
from fastapi_pagination import Page, Params, paginate


router = APIRouter(tags=["authors"], prefix="/authors")


@router.post("/", response_model=AuthorDB)
async def create_author(payload: AuthorCreate, author_crud: AuthorCrud = Depends(get_author_crud)) -> AuthorDB:
    res = await author_crud.create_author(payload=payload)
    return res


@router.get("/", status_code=status.HTTP_200_OK, response_model = Page[AuthorDB])
async def get_all_authors(author_crud: AuthorCrud = Depends(get_author_crud), params: Params = Depends()) -> Page[AuthorDB]:
    res = await author_crud.get_all_authors()
    return paginate(res, params)


@router.get("/{author_id}", status_code=status.HTTP_200_OK, response_model = AuthorDB)
async def get_author_by_id(author_id: int, author_crud: AuthorCrud = Depends(get_author_crud)) -> AuthorDB:
    res = await author_crud.get_author_by_id(author_id=author_id)
    return res


@router.put("/{author_id}", status_code=status.HTTP_200_OK, response_model=AuthorDB)
async def update_author(payload: AuthorUpdate, author_id: int, author_crud: AuthorCrud = Depends(get_author_crud)) -> AuthorDB:
    res = await author_crud.update_author(author_id=author_id, payload=payload)
    return res


@router.delete("/{author_id}",  status_code=status.HTTP_200_OK, response_model=AuthorDB)
async def delete_author(author_id: int, author_crud: AuthorCrud = Depends(get_author_crud)) -> AuthorDB:
    res = await author_crud.delete_author(author_id=author_id)
    return res
