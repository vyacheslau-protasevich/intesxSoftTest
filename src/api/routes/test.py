from fastapi import APIRouter, Depends, HTTPException, UploadFile, Form, File
from starlette import status


router = APIRouter(
    tags=["Starting test router"], prefix="/api/test"
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_hello():
    return {"Hello, user"}
