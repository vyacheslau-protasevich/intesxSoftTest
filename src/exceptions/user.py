class UserDoesNotExistError(Exception):

    def __init__(self, id: str) -> None:
        super().__init__(f"User with id='{id}' does not exist")


class NoUpdateDataProvidedError(Exception):

    def __init__(self) -> None:
        super().__init__("No update data provided")


class NoPathFoundError(Exception):

    def __init__(self, user_id_1: str, user_id_2: str) -> None:
        super().__init__(f"No path found between users with id='{user_id_1}' and id='{user_id_2}'")


class UsersAreAlreadyFriendsError(Exception):

    def __init__(self, user_id_1: str, user_id_2: str) -> None:
        super().__init__(f"Users with id='{user_id_1}' and id='{user_id_2}' are already friends")


class CannotMakeFriendsWithSelfError(Exception):

    def __init__(self) -> None:
        super().__init__("Cannot make friends with self")


class ToManyFriendsToCreateError(Exception):

    def __init__(self) -> None:
        super().__init__("Cannot make friends with such amount of users")
