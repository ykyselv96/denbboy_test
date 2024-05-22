from fastapi import APIRouter, Depends, status
from schemas.categories_schema import CategoryBase, CategoryCreate, CategoryDB, CategoryUpdate
from crud.category_crud import CategoryCrud, get_category_crud
from fastapi_pagination import Page, Params, paginate



router = APIRouter(tags=["categories"], prefix="/categories")


@router.post("/", response_model=CategoryDB)
async def create_category(payload: CategoryCreate, category_crud: CategoryCrud = Depends(get_category_crud)) -> CategoryDB:
    res = await category_crud.create_category(payload)
    return res


@router.get("/", status_code=status.HTTP_200_OK, response_model = Page[CategoryDB])
async def get_all_categories(category_crud: CategoryCrud = Depends(get_category_crud), params: Params = Depends()) -> Page[CategoryDB]:
    res = await category_crud.get_all_categories()
    return paginate(res, params)


@router.get("/{category_id}", status_code=status.HTTP_200_OK, response_model = CategoryDB)
async def get_category_by_id(category_id: int, category_crud: CategoryCrud = Depends(get_category_crud)) -> CategoryDB:
    res = await category_crud.get_category_by_id(category_id=category_id)
    return res


@router.put("/{category_id}", status_code=status.HTTP_200_OK, response_model=CategoryDB)
async def update_category(payload: CategoryUpdate, category_id: int, category_crud: CategoryCrud = Depends(get_category_crud)) -> CategoryDB:
    res = await category_crud.update_category(category_id=category_id, payload=payload)
    return res


@router.delete("/{category_id}",  status_code=status.HTTP_200_OK, response_model=CategoryDB)
async def delete_category(category_id: int, category_crud: CategoryCrud = Depends(get_category_crud)) -> CategoryDB:
    res = await category_crud.delete_category(category_id=category_id)
    return res
