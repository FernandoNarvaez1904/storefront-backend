FROM pypy

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY requirements.txt /code/

RUN pypy -m ensurepip
RUN pypy -m pip install -r requirements.txt

COPY . /code/

EXPOSE 8080

RUN pypy manage.py migrate

CMD gunicorn -k uvicorn.workers.UvicornWorker storefront_backend.asgi:application