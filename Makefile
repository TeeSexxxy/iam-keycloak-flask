.PHONY: reset up down logs test

reset: down
	docker volume rm home8_iam_postgres_data || true
	docker-compose up --build -d
	@echo "✅ Environment reset and containers started."

up:
	docker-compose up --build -d

down:
	docker-compose down -v

logs:
	docker-compose logs -f

test:
	./test_api_noparse.sh
