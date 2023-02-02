FROM python:3.10.9

RUN apt-get update

RUN useradd -ms /bin/bash myuser

ENV POETRY_VERSION=1.3

RUN pip install poetry==$POETRY_VERSION

WORKDIR /code
COPY . /code

RUN chown -R myuser /code

USER myuser

RUN poetry install