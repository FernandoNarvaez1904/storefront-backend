# base image
FROM pypy:3.9

# setup environment variable
ENV DockerHOME=/home/app/app

# set work directory
RUN mkdir -p $DockerHOME

# where your code lives
WORKDIR $DockerHOME

COPY requirements.txt .

RUN pypy -m pip install -r requirements.txt

COPY . .

CMD ["pypy", "run_server.py"]