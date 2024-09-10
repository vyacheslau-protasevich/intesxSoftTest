run-uvicorn:
	cd src && uvicorn main:app --reload

run:
	cd src && \
	gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

docker-build:
	docker compose build

docker-run:
	docker compose up --build

lint:
	flake8 src/

run-test-db:
	cd tests/docker && docker-compose up --build -d


stop-test-db:
	docker stop neo4j_db_test


test:
	pytest -s -v \
	tests/api/test_users.py \
	tests/api/test_random.py \
	tests/api/test_friends.py \
