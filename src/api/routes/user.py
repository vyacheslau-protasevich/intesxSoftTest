from uuid import UUID

from fastapi import APIRouter, Depends, Form, Response, HTTPException
from starlette import status

from api.dependencies.db import get_user_service
from models.user import UserIn, UserOut, UserUpdate, UserUpdateIn
from services.db.user import UserService


router = APIRouter(
    tags=["Users"], prefix="/api/users"
)


@router.post("", status_code=status.HTTP_201_CREATED)
async def create_user(
        user: UserIn,
        user_service: UserService = Depends(get_user_service),
):
    await user_service.create_user(user)
    return {
        "status": "User created"
    }


@router.get("/{user_id}", status_code=status.HTTP_200_OK, summary="Get user by id")
async def get_my_profile(
        user_id: UUID,
        user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_current_user(user_id)
    return await user_service.get_user_by_id(user_id)


@router.put("/{user_id}", status_code=status.HTTP_202_ACCEPTED)
async def update_user(
        user_id: UUID,
        first_name: str | None = Form(None),
        last_name: str | None = Form(None),
        phone: int | None = Form(None),
        address: str | None = Form(None),
        city: str | None = Form(None),
        state: str | None = Form(None),
        zipcode: int | None = Form(None),
        profile_photo: str | None = Form(None),
        user_service: UserService = Depends(get_user_service),
):
    if phone:
        try:
            phone = int(phone)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid phone number format.")

    if zipcode:
        try:
            zipcode = int(zipcode)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid zipcode format.")
    user = await user_service.get_current_user(user_id)
    update_data = UserUpdateIn(
        first_name=first_name,
        last_name=last_name,
        phone=phone,
        address=address,
        city=city,
        state=state,
        zipcode=zipcode,
        profile_photo=profile_photo
    )

    await user_service.update_user(user_id, update_data)
    return Response(status_code=status.HTTP_200_OK)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
        user_id: UUID,
        user_service: UserService = Depends(get_user_service),
):
    user = await user_service.get_current_user(user_id)
    await user_service.delete_user(user_id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
