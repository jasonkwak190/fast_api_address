from fastapi import APIRouter
from api.v1.endpoints.download import router as download_and_extract

router = APIRouter()

router.include_router(download_and_extract, tags=['파일 다운로드'])

