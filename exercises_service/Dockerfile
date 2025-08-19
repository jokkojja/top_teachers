FROM python:3.11.2-slim-buster


RUN apt-get update && apt-get install ffmpeg libsm6 libxext6 -y && \
  pip install --no-cache-dir --upgrade --root-user-action ignore pip setuptools wheel poetry && \
  useradd -ms /bin/bash exercises_service && \
  rm -rf /var/lib/apt/lists/* && \
  poetry config virtualenvs.create false

WORKDIR /app/exercises

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --without=dev

COPY . .

USER exercises_service
ENTRYPOINT ["poetry", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
