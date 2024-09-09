from neo4j import Session
from models.user import UserIn, UserUpdateIn, UserOut
from exceptions.user import UserDoesNotExistError, NoUpdateDataProvidedError, NoPathFoundError, UsersAreAlreadyFriendsError

import uuid
from datetime import datetime

import logging


class Neo4jService:

    def __init__(self, session: Session) -> None:
        self.session = session

    def create_user(self, user_data: UserIn):
        user_id = str(uuid.uuid4())
        self.session.run(
                """
                CREATE (u:User {id: $id, first_name: $first_name, last_name: $last_name,
                                phone: $phone, address: $address, city: $city, state: $state,
                                zipcode: $zipcode, available: $available, profile_photo_url: $profile_photo_url,
                                created_at: $created_at})
                """,
                id=user_id,
                first_name=user_data.first_name,
                last_name=user_data.last_name,
                phone=user_data.phone,
                address=user_data.address,
                city=user_data.city,
                state=user_data.state,
                zipcode=user_data.zipcode,
                available=user_data.available,
                profile_photo_url=user_data.profile_photo_url,
                created_at=datetime.utcnow()
            )
        return {"id": user_id}

    def delete_user_by_id(self, user_id: uuid.UUID) -> None:
        user = self.get_user_by_id(user_id)
        self.session.run(
                """
                MATCH (u:User {id: $id}) DETACH DELETE u
                """, id=str(user_id)
            )

    def update_user_by_id(self, user_id: uuid.UUID, user_update: UserUpdateIn) -> None:
        user = self.get_user_by_id(user_id)

        update_data = user_update.model_dump(exclude_unset=True, exclude_none=True)

        if not update_data:
            raise NoUpdateDataProvidedError

        query = "MATCH (u:User {id: $id}) SET "
        query_params = {"id": str(user_id)}

        for key, value in update_data.items():
            query += f"u.{key} = ${key}, "
            query_params[key] = value

        query = query.rstrip(", ")
        query += " RETURN u"

        result = self.session.run(query, **query_params)
        updated_user = result.single()

        if updated_user:
            return
        raise UserDoesNotExistError(id=str(user_id))

    def get_user_by_id(self, user_id: uuid.UUID) -> UserOut:
        result = self.session.run(
            """
            MATCH (u:User {id: $id}) RETURN u
            """, id=str(user_id)
        )
        if not result.single():
            raise UserDoesNotExistError(id=str(user_id))
        user = dict(result.single()["u"].items())
        user["created_at"] = user["created_at"].to_native()
        return UserOut(**user)

    def get_all_users(self) -> list[UserOut]:
        result = self.session.run(
            """
            MATCH (u:User) RETURN u
            """
        )
        users = []
        for record in result:
            user_data = dict(record["u"].items())
            user_data["created_at"] = user_data["created_at"].to_native()
            users.append(UserOut(**user_data))
        return users

    def make_friends(self, user_id_1: uuid.UUID, user_id_2: uuid.UUID) -> None:
        user_1 = self.get_user_by_id(user_id_1)
        user_2 = self.get_user_by_id(user_id_2)

        friendship_exists = self.session.run(
            """
            MATCH (u1:User {id: $user_id_1})-[:FRIEND]-(u2:User {id: $user_id_2})
            RETURN u1
            """,
            user_id_1=str(user_id_1),
            user_id_2=str(user_id_2)
        ).single()

        if friendship_exists:
            raise UsersAreAlreadyFriendsError(user_id_1=str(user_id_1), user_id_2=str(user_id_2))

        self.session.run(
            """
            MATCH (u1:User {id: $user_id_1}), (u2:User {id: $user_id_2})
            CREATE (u1)-[:FRIEND]->(u2)
            CREATE (u2)-[:FRIEND]->(u1)
            """,
            user_id_1=str(user_id_1),
            user_id_2=str(user_id_2)
        )

    def get_friends(self, user_id: uuid.UUID) -> list[str]:
        user = self.get_user_by_id(user_id)
        result = self.session.run(
            """
            MATCH (u:User {id: $id})-[:FRIEND]->(friend)
            RETURN friend
            """, id=str(user_id)
        )
        friends = [record["friend"]["id"] for record in result]
        return friends

    def get_shortest_path(self, user_id_1: uuid.UUID, user_id_2: uuid.UUID) -> list[str]:
        user_1 = self.get_user_by_id(user_id_1)
        user_2 = self.get_user_by_id(user_id_2)
        result = self.session.run(
            """
            MATCH p=shortestPath((u1:User {id: $user_id_1})-[:FRIEND*]-(u2:User {id: $user_id_2}))
            RETURN p
            """, user_id_1=str(user_id_1), user_id_2=str(user_id_2)
        )
        path = result.single()

        if path:
            user_nodes = path["p"].nodes
            path_users = [node["id"] for node in user_nodes]
            return path_users[1:-1]
        else:
            raise NoPathFoundError(user_id_1=str(user_id_1), user_id_2=str(user_id_2))
