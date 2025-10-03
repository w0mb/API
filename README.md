
docker network create myNetwork

docker run --name booking_db \
    -p 6432:5433 \
    -e POSTGRES_USER=abcde \
    -e POSTGRES_PASSWORD=abcde \
    -e POSTGRES_DB=booking \
    --volume pg-booking-data:/var/lib/postgresql/data \
    -d postgres:16 -p 5433

docker run --name booking_cache \
    -p 7379:6379 \
    -d redis:7.4

docker run --name booking_back \
    -p 7777:8000 \
    booking_image


docker run --name booking_celery_worker \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO


docker run --name booking_celery_beat \
    booking_image \
    celery --app=src.tasks.celery_app:celery_instance worker -l INFO -B


docker build -t booking_image .