from uuid import UUID

from exceptions.user import UserDoesNotExistError, NoPathFoundError, UsersAreAlreadyFriendsError
from fastapi import APIRouter, Depends, Form, Response, HTTPException
from services.db.db import Neo4jService
from starlette import status

from api.dependencies.db import get_neo4j_sevice
from models.user import UserIn, UserOut, UserUpdate, UserUpdateIn


router = APIRouter(
    tags=["Friends"], prefix="/api/friends"
)


@router.get("/all_friends", status_code=status.HTTP_200_OK)
def all_users_friends(
        user_id: UUID,
        neo4j_service: Neo4jService = Depends(get_neo4j_sevice),
):
    try:
        return neo4j_service.get_friends(user_id=user_id)
    except UserDoesNotExistError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.post("/make_friends", status_code=status.HTTP_201_CREATED)
def make_friends(
        user_id_1: UUID,
        user_id_2: UUID,
        neo4j_service: Neo4jService = Depends(get_neo4j_sevice),
):
    try:
        neo4j_service.make_friends(user_id_1=user_id_1, user_id_2=user_id_2)
        return Response(status_code=status.HTTP_201_CREATED)
    except UserDoesNotExistError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UsersAreAlreadyFriendsError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@router.get("/shortest_path", status_code=status.HTTP_200_OK)
def shortest_path(
        user_id_1: UUID,
        user_id_2: UUID,
        neo4j_service: Neo4jService = Depends(get_neo4j_sevice),
):
    try:
        return neo4j_service.get_shortest_path(user_id_1=user_id_1, user_id_2=user_id_2)
    except UserDoesNotExistError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except NoPathFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

