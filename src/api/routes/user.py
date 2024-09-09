from uuid import UUID

from exceptions.user import UserDoesNotExistError
from fastapi import APIRouter, Depends, Form, Response, HTTPException
from services.db.db import Neo4jService
from starlette import status

from api.dependencies.db import get_neo4j_sevice
from models.user import UserIn, UserOut, UserUpdate, UserUpdateIn


router = APIRouter(
    tags=["Users"], prefix="/api/users"
)


@router.post("", status_code=status.HTTP_201_CREATED)
def create_user(
        user: UserIn,
        neo4j_service: Neo4jService = Depends(get_neo4j_sevice),
):
    return neo4j_service.create_user(user)


@router.get("/{user_id}", status_code=status.HTTP_200_OK, summary="Get user by id")
def get_user_profile(
        user_id: UUID,
        neo4j_service: Neo4jService = Depends(get_neo4j_sevice),
):
    try:
        return neo4j_service.get_user_by_id(user_id)
    except UserDoesNotExistError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


@router.get("/all_users", status_code=status.HTTP_200_OK)
def get_all_users(
        neo4j_service: Neo4jService = Depends(get_neo4j_sevice),
):
    return neo4j_service.get_all_users()


@router.put("/{user_id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(
        user_id: UUID,
        first_name: str | None = Form(None),
        last_name: str | None = Form(None),
        phone: int | None = Form(None),
        address: str | None = Form(None),
        city: str | None = Form(None),
        state: str | None = Form(None),
        zipcode: int | None = Form(None),
        profile_photo: str | None = Form(None),
        neo4j_service: Neo4jService = Depends(get_neo4j_sevice),
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
    try:
        neo4j_service.update_user_by_id(user_id, update_data)
    except UserDoesNotExistError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return Response(status_code=status.HTTP_200_OK)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
        user_id: UUID,
        neo4j_service: Neo4jService = Depends(get_neo4j_sevice),
):
    try:
        neo4j_service.delete_user_by_id(user_id)
    except UserDoesNotExistError:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)
