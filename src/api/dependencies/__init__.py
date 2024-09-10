from fastapi import FastAPI
from neo4j import Driver

from api.dependencies.stubs import get_neo4j_driver


def setup_dependencies(app: FastAPI, neo4j_driver: Driver) -> None:
    app.dependency_overrides[get_neo4j_driver] = lambda: neo4j_driver
