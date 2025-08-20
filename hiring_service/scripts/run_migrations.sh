#!/bin/sh

# if [ "$RUN_MIGRATIONS" = "true" ]; then
echo "Запуск миграций..."
alembic upgrade head
# else
# echo "Миграции пропущены"
# fi
