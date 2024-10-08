from uuid import UUID

from exceptions.user import UserDoesNotExistError, NoUpdateDataProvidedError
from fastapi import APIRouter, Depends, Form, Response, HTTPException
from services.db.db import Neo4jService
from starlette import status

from api.dependencies.db import get_neo4j_service
from models.user import UserIn, UserUpdateIn, UserOut

router = APIRouter(
    tags=["Users"], prefix="/api/users"
)


@router.post("",
             response_model=dict[str, str],
             status_code=status.HTTP_201_CREATED
             )
def create_user(
        user: UserIn,
        neo4j_service: Neo4jService = Depends(get_neo4j_service),
):
    return neo4j_service.create_user(user)


@router.get("/all_users",
            response_model=list[UserOut],
            status_code=status.HTTP_200_OK,
)
def get_all_users(
        neo4j_service: Neo4jService = Depends(get_neo4j_service),
):
    return neo4j_service.get_all_users()


@router.get(
    "/{user_id}",
    response_model=UserOut,
    status_code=status.HTTP_200_OK,
    summary="Get user by id"
)
def get_user_profile(
        user_id: UUID,
        neo4j_service: Neo4jService = Depends(get_neo4j_service),
):
    try:
        return neo4j_service.get_user_by_id(user_id)
    except UserDoesNotExistError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )


@router.put("/{user_id}", status_code=status.HTTP_202_ACCEPTED)
def update_user(
        user_id: UUID,
        first_name: str | None = Form(None),
        last_name: str | None = Form(None),
        phone: int | None = Form(None),
        address: str | None = Form(None),
        city: str | None = Form(None),
        state: str | None = Form(None, min_length=2, max_length=2),
        zipcode: int | None = Form(None),
        profile_photo: str | None = Form(None),
        neo4j_service: Neo4jService = Depends(get_neo4j_service),
):
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
    except UserDoesNotExistError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(e)
        )
    except NoUpdateDataProvidedError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail=str(e))
    return Response(status_code=status.HTTP_200_OK)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, )
def delete_user(
        user_id: UUID,
        neo4j_service: Neo4jService = Depends(get_neo4j_service),
):
    try:
        neo4j_service.delete_user_by_id(user_id)
    except UserDoesNotExistError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=str(e))
    return Response(status_code=status.HTTP_204_NO_CONTENT)
