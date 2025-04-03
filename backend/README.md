# Lesta Backend

The service uses the following technologies:


- `python ^3.13`
- `poetry ==2.1.2`
- `django >=5.2.0,<6.0.0`
- `postgres ^17.0,<18.0`


## How to run local environment via docker
```sh
$ git clone https://github.com/aeSYNK/lesta-backend.git
$ cp .env.sample .env
$ docker-compose -f docker-compose.yml up --build -d
$ docker-compose logs # For see containers logs.
```

## How to run local environment via local machine
```sh
$ activate venv
$ pip install poetry
$ cd backend
$ poetry install
$ pyhton manage.py migrate
$ pyhton manage.py runserver
```
