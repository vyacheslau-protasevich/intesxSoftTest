from fastapi import FastAPI

from api.routes import user
from api.routes import friends
from api.routes import random


def setup_routes(app: FastAPI) -> None:
    app.include_router(user.router)
    app.include_router(friends.router)
    app.include_router(random.router)
