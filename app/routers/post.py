from fastapi import APIRouter, Depends, status
from schemas.posts_schema import PostCreate, PostDB, PostBase, PostUpdate
from crud.post_crud import PostCrud, get_post_crud
from fastapi_pagination import Page, Params, paginate



router = APIRouter(tags=["posts"], prefix="/posts")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostDB)
async def create_post(payload: PostCreate, post_crud: PostCrud = Depends(get_post_crud)) -> PostDB:
    res = await post_crud.create_post(payload=payload)
    return res


@router.get("/", status_code=status.HTTP_200_OK, response_model = Page[PostDB])
async def get_all_posts(post_crud: PostCrud = Depends(get_post_crud), params: Params = Depends()) -> Page[PostDB]:
    res = await post_crud.get_all_posts()
    return paginate(res, params)

@router.get("/{post_id}", status_code=status.HTTP_200_OK, response_model = PostDB)
async def get_post_by_id(post_id: int, post_crud: PostCrud = Depends(get_post_crud)) -> PostDB:
    res = await post_crud.get_post_by_id(post_id=post_id)
    return res

@router.put("/{post_id}", status_code=status.HTTP_200_OK, response_model=PostDB)
async def update_post(payload: PostUpdate, post_id: int, post_crud: PostCrud = Depends(get_post_crud)) -> PostDB:
    res = await post_crud.update_post(post_id=post_id, payload=payload)
    return res

@router.delete("/{post_id}",  status_code=status.HTTP_200_OK, response_model=PostDB)
async def delete_post(post_id: int, post_crud: PostCrud = Depends(get_post_crud)) -> PostDB:
    res = await post_crud.delete_post(post_id=post_id)
    return res