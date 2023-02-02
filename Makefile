include .env

cli:
	@poetry run python cli.py

docker-build:
	@docker build -t flight-finder .

docker-run:
	@docker run -ti -v $(shell pwd)/cache:/code/cache -e API_KEY=$(API_KEY) -e API_SECRET=$(API_SECRET) -e API_URL=$(API_URL) flight-finder /bin/sh -c 'poetry run python cli.py'