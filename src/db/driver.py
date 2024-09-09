from neo4j import GraphDatabase, Driver


def get_neo4j_driver(neo4j_uri: str, username: str, password: str) -> Driver:
    return GraphDatabase.driver(neo4j_uri, auth=(username, password))