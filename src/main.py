from fastapi import FastAPI

# from api.dependencies import setup_dependencies
from api.routes import setup_routes
from api.dependencies import setup_dependencies
from config import Settings
from db.driver import get_neo4j_driver


def create_app() -> FastAPI:

    app = FastAPI(
        title="Test API",
        version="1.0"
    )

    config = Settings()
    neo4j_driver = get_neo4j_driver(
        neo4j_uri=config.neo4j_uri,
        username=config.neo4j_user,
        password=config.neo4j_password
    )

    setup_dependencies(
        app=app,
        neo4j_driver=neo4j_driver
    )
    setup_routes(app)

    return app


app = create_app()
