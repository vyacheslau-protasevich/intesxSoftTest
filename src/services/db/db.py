from neo4j import Session
from models.user import UserIn, UserUpdateIn, UserOut
from exceptions.user import UserDoesNotExistError, NoUpdateDataProvidedError

import uuid


class Neo4jService:

    def __init__(self, session: Session) -> None:
        self.session = session

    def create_user(self, user_data: UserIn):
        """Create a new user based on the UserIn model."""
        user_id = str(uuid.uuid4())
        self.session.run(
                """
                CREATE (u:User {id: $id, first_name: $first_name, last_name: $last_name,
                                phone: $phone, address: $address, city: $city, state: $state,
                                zipcode: $zipcode, available: $available, profile_photo_url: $profile_photo_url})
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
                profile_photo_url=user_data.profile_photo_url
            )
        return {"id": user_id, "message": "User created successfully"}

    def delete_user_by_id(self, user_id: uuid.UUID):
        """Delete a user by their ID."""
        user = self.get_user_by_id(user_id)
        self.session.run(
                """
                MATCH (u:User {id: $id}) DETACH DELETE u
                """, id=str(user_id)
            )

    def update_user_by_id(self, user_id: uuid.UUID, user_update: UserUpdateIn):
        """Update user properties by their ID."""
        user = self.get_user_by_id(user_id)

        # Convert Pydantic model to a dictionary and filter out None values
        update_data = user_update.model_dump(exclude_unset=True, exclude_none=True)

        if not update_data:
            raise NoUpdateDataProvidedError

        query = "MATCH (u:User {id: $id}) SET "
        query_params = {"id": str(user_id)}

        # Dynamically build the query based on the provided update data
        for key, value in update_data.items():
            query += f"u.{key} = ${key}, "
            query_params[key] = value

        query = query.rstrip(", ")  # Remove trailing comma
        query += " RETURN u"

        # Execute the query
        result = self.session.run(query, **query_params)
        updated_user = result.single()

        if updated_user:
            return
        raise UserDoesNotExistError

    def get_user_by_id(self, user_id: uuid.UUID) -> UserOut:
        """Retrieve a user by their ID."""
        result = self.session.run(
            """
            MATCH (u:User {id: $id}) RETURN u
            """, id=str(user_id)
        )
        user = result.single()
        if user:
            return UserOut(**user["u"], id=user_id)
        else:
            raise UserDoesNotExistError

    def get_all_users(self):
        """Retrieve a list of all users."""
        result = self.session.run(
            """
            MATCH (u:User) RETURN u
            """
        )
        users = [record["u"] for record in result]
        return {"users": users}

    def make_friends(self, user_id_1: uuid.UUID, user_id_2: uuid.UUID):
        """Create a friendship relationship between two users."""
        user_1 = self.get_user_by_id(user_id_1)
        user_2 = self.get_user_by_id(user_id_2)
        self.session.run(
            """
            MATCH (u1:User {id: $user_id_1}), (u2:User {id: $user_id_2})
            CREATE (u1)-[:FRIEND]->(u2), (u2)-[:FRIEND]->(u1)
            """, user_id_1=str(user_id_1), user_id_2=str(user_id_2)
        )
        return {"message": f"User {user_id_1} and {user_id_2} are now friends"}

    def get_friends(self, user_id: uuid.UUID):
        """Retrieve all friends of a specific user."""
        user = self.get_user_by_id(user_id)
        result = self.session.run(
            """
            MATCH (u:User {id: $id})-[:FRIEND]->(friend)
            RETURN friend
            """, id=str(user_id)
        )
        friends = [record["friend"] for record in result]
        return {"friends": friends}

    def get_shortest_path(self, user_id_1: uuid.UUID, user_id_2: uuid.UUID):
        """Find the shortest path between two users."""
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
            path_users = [{"id": node["id"], "first_name": node["first_name"], "last_name": node["last_name"]} for
                          node in user_nodes]
            return {"path": path_users}
        else:
            return {"error": "No path found between users"}
