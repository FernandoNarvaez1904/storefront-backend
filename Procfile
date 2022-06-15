release: python manage.py migrate
web: gunicorn -k uvicorn.workers.UvicornWorker social_media_backend.asgi:application