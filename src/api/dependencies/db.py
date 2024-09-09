from typing import Any, Generator

from fastapi import Depends
from neo4j import Driver

from api.dependencies.stubs import get_neo4j_driver
from services.db.db import Neo4jService


def get_neo4j_sevice(
    neo4j_driver: Driver = Depends(get_neo4j_driver)
) -> Generator[Neo4jService, Any, None]:
    with neo4j_driver.session() as session:
        yield Neo4jService(session=session)