FROM python:3.11-slim-bullseye

RUN apt-get update && apt-get install -y \
  gcc \
  libpq-dev \
  python3-dev && \
  useradd -ms /bin/bash hiring_service && \
  rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade --root-user-action=ignore pip setuptools wheel poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry config virtualenvs.create false \
  && poetry install --no-root

COPY . ./

RUN chown -R hiring_service:hiring_service /app

USER hiring_service

RUN chmod +x ./scripts/run_migrations.sh

# CMD [ "sh", "-c", "./scripts/run_migrations.sh" ]
# ENTRYPOINT [ "sh", "-c", "./scripts/run_migrations.sh" ]

# ENTRYPOINT ["sh", "-c", "python3 __main__.py"]
# FIXME: Fix this shit with migrations depends on kafka container
ENTRYPOINT ["sh", "-c", "./scripts/run_migrations.sh && python3 __main__.py"]
