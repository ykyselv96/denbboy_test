from fastapi import FastAPI
from routers import author, category, post, tag
import uvicorn
from core.config import settings
from loguru import logger
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI()


origins = ["http://localhost",
           "http://localhost:8000",
           ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup():
    logger.info("startup")

@app.on_event("shutdown")
async def shutdown():
    logger.info("shutdown")


app.include_router(author.router)
app.include_router(category.router)
app.include_router(tag.router)
app.include_router(post.router)


if __name__ == "__main__":
    uvicorn.run('main:app', host=settings.app_host, port=int(settings.app_port), reload=True)
