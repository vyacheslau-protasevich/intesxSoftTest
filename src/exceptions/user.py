class UserDoesNotExistError(Exception):

    def __init__(self, id: str) -> None:
        super().__init__(f"User with id='{id}' does not exist")


class NoUpdateDataProvidedError(Exception):

    def __init__(self) -> None:
        super().__init__("No update data provided")
