class UserDoesNotExistError(Exception):

    def __init__(self, id: str) -> None:
        super().__init__(f"User with id='{id}' does not exist")
