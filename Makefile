up:
	docker compose --env-file .env up  --build -d

down:
	docker compose --env-file .env down

sh: 
	docker exec -it container_name bash

run-etl:
	docker exec container_name python loader_script.py

warehouse:
	docker exec -it warehouse psql postgres://thierros:thierros@localhost:5432/warehouse