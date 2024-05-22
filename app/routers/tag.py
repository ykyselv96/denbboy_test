from fastapi import APIRouter, Depends, status
from schemas.tags_schema import TagCreate, TagDB, TagBase, TagUpdate
from crud.tag_crud import TagCrud, get_tag_crud
from fastapi_pagination import Page, Params, paginate



router = APIRouter(tags=["tags"], prefix="/tags")


@router.post("/", response_model=TagDB)
async def create_tag(payload: TagCreate, tag_crud: TagCrud = Depends(get_tag_crud)) -> TagDB:
    res = await tag_crud.create_tag(payload=payload)
    return res


@router.get("/", status_code=status.HTTP_200_OK, response_model = Page[TagDB])
async def get_all_tags(tag_crud: TagCrud = Depends(get_tag_crud), params: Params = Depends()) -> Page[TagDB]:
    res = await tag_crud.get_all_tags()
    return paginate(res, params)


@router.get("/{tag_id}", status_code=status.HTTP_200_OK, response_model = TagDB)
async def get_tag_by_id(tag_id: int, tag_crud: TagCrud = Depends(get_tag_crud)) -> TagDB:
    res = await tag_crud.get_tag_by_id(tag_id=tag_id)
    return res


@router.put("/{tag_id}", status_code=status.HTTP_200_OK, response_model=TagDB)
async def update_tag(payload: TagUpdate, tag_id: int, tag_crud: TagCrud = Depends(get_tag_crud)) -> TagDB:
    res = await tag_crud.update_tag(payload=payload, tag_id=tag_id)
    return res


@router.delete("/{tag_id}",  status_code=status.HTTP_200_OK, response_model=TagDB)
async def delete_tag(tag_id: int, tag_crud: TagCrud = Depends(get_tag_crud)) -> TagDB:
    res = await tag_crud.delete_tag(tag_id=tag_id)
    return res
