FROM python:3.12-slim

LABEL maintainer="andreybibea@gmail.com"
LABEL varsion="0.2.0"

WORKDIR /app

# Install dependencies
COPY poetry.lock pyproject.toml /app/
RUN pip install poetry==1.8.3 && \
    poetry config virtualenvs.create false && \
    poetry install --no-root --no-interaction

# Project files
COPY src/ /app/src

CMD ["python3",  "-m", "src"]
