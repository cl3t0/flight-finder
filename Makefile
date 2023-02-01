include .env

run:
	@poetry run python main.py

docker-build:
	@docker build -t flight-finder .

docker-run:
	@docker run --env API_KEY=$(API_KEY) --env API_SECRET=$(API_SECRET) --env API_URL=$(API_URL) flight-finder