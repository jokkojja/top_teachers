.PNONY: up down

run:
	docker compose -f docker-compose-dev.yaml up --build

down:
	docker compose -f docker-compose-dev.yaml down -v
