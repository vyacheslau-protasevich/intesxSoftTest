from exceptions.user import ToManyFriendsToCreateError
from fastapi import APIRouter, Depends, HTTPException
from services.db.db import Neo4jService
from starlette import status

from api.dependencies.db import get_neo4j_sevice


router = APIRouter(
    tags=["Random"], prefix="/api/random"
)


@router.post("/random_{users}_users_{friends}_friends", status_code=status.HTTP_200_OK)
def create_random_users_and_make_friends(
        users: int,
        friends: int,
        neo4j_service: Neo4jService = Depends(get_neo4j_sevice),
):
    try:
        neo4j_service.create_random_profiles(num_profiles=users, total_friends=friends)
    except ToManyFriendsToCreateError as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
