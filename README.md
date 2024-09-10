# IntexSoft test task

## Run application:
- Create `.env` file following `.env.example`
- Run docker compose:
```
docker compose up --build
```
- SwaggerUI will be accessible by `http://127.0.0.1:8000/docs`

## Runnig tests:
- Tests have to be run while the application is NOT running
- Run test db:
```
make run-test-db
```
- Run tests:
```
make test
```
- Stop test db:
```
make stpo-test-db
```


## Used technologies:
- Python 3.11
- FastAPI
- Pydantic
- Neo4j
- Docker
- Pytest



[Description of application's maintainability, scalability, and reliability:](https://docs.google.com/document/d/127Y35hXNezkkHjo18KLaSGPSkwwKTUT7W3SEarKsmpQ/edit?usp=sharing)

