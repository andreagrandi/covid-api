# covid-api
COVID19 Api based on Johns Hopkins CSSE data

The intent of this project is to create an API which will make easier to access the COVID19 reports provided by the Johns Hopkins CSSE: https://github.com/CSSEGISandData/COVID-19

# Status

We are in the early phase of the project and framework, architectural and other decisions haven't been taken yet. Please help discussing them in the GitHub **Issues** section of this project.

# Project setup

## Postgres database
You will need a postgres database to run the application.
If you have [docker](https://docs.docker.com/get-started/) installed, then you can create a database by running

```
docker-compose up db
```

This creates an empty database called `covidapi`, and a user called `covidapi` with password `dummypassword`.

## Running the app through docker
If you run `docker-compose up` instead of `docker-compose up db`, the whole app will be run inside docker as well.

The first time you do this you will need to run `docker-compose exec app python /covidapi/covidapi/import_data.py` to import the data.

## Running the app directly
To run the app directly you will need python 3.7 or later.

Create a virtualenv, activate it, and then install the dependencies:

```
python -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

To import the data, run

```
python covidapi/import_data.py
```

Then you can run the app with:

```
uvicorn covidapi.app:app --reload
```

## Viewing the API
The API will be served at [http://localhost:8000/](http://localhost:8000/)

The API docs are served at [http://localhost:8000/docs](http://localhost:8000/docs)

## Deployment
See [deploying to heroku](./docs/heroku-deploy.md).
