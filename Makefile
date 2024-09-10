run-uvicorn:
	cd src && uvicorn main:app --reload

run:
	cd src && \
	gunicorn main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

docker-build:
	docker compose build

docker-run:
	docker compose up

lint:
	flake8 src/

test:
	pytest -s -v \
	tests/api/test_users.py \
	tests/api/test_random.py \
	tests/api/test_friends.py \
