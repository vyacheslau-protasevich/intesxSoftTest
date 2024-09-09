from fastapi import FastAPI

from api.routes import test
from api.routes import user
from api.routes import friends


def setup_routes(app: FastAPI) -> None:
    app.include_router(test.router)
    app.include_router(user.router)
    app.include_router(friends.router)
