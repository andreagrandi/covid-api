# covid-api

COVID19 Api based on Johns Hopkins CSSE data (more data sources are coming).

[![CircleCI](https://circleci.com/gh/andreagrandi/covid-api.svg?style=svg)](https://circleci.com/gh/andreagrandi/covid-api)

The intent of this project is to create an API which will make easier to access the COVID19 reports provided by the Johns Hopkins CSSE and other data sources available.
Using this API researchers can concentrate their efforts on data analysis while we take care of retriving the data, cleaning it and keeping the database always updated.

# Data Sources

- Johns Hopkins CSSE: https://github.com/CSSEGISandData/COVID-19

# Status

We have essentially reached an MVP status (see #20 for more information) and live data is available at https://api.covid19data.cloud

Now we are working on improving features (like adding more query filters for existing endpoints) and better cleaning the available data.

The next step will be to add more data sources.

# Usage Example (Python)

```
In [1]: import requests

In [2]: response = requests.get('https://api.covid19data.cloud/v1/jh/daily-reports?last_update_from=2020-04-01&last_update_to=2020-04-03&country=Italy')

In [3]: response.json()
Out[3]:
[{'id': 35343,
  'country_region': 'Italy',
  'province_state': None,
  'fips': None,
  'admin2': None,
  'last_update': '2020-04-01T21:58:34',
  'confirmed': 110574,
  'deaths': 13155,
  'recovered': 16847},
 {'id': 37895,
  'country_region': 'Italy',
  'province_state': None,
  'fips': None,
  'admin2': None,
  'last_update': '2020-04-02T23:25:14',
  'confirmed': 115242,
  'deaths': 13915,
  'recovered': 18278}]
```

Further API documentation is available at https://api.covid19data.cloud/docs

# Development Setup

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
python import_data.py jh --all
```

Then you can run the app with:

```
uvicorn covidapi.app:app --reload
```

## Viewing the API
The API will be served at [http://localhost:8000/](http://localhost:8000/)

The API docs are served at [http://localhost:8000/docs](http://localhost:8000/docs)

## Deployment
The lastest `master` branch is automatically deployed to Heroku whenever a pull request is merged (and tests are passing on CircleCI).

See [deploying to heroku](./docs/heroku-deploy.md).

# Sponsors and Thanks

- [Heroku](https://www.heroku.com): for sponsoring the costs of running the service

# Disclaimer

We are doing our best to keep the available data updated, clean (removing duplicates), and to provide a reliable service, but we are not in any way responsible for the accuracy of the data nor for the availability of the service itself. Please **use it at your own risk**.

**Abuse notice:** we are currently not requiring any registration or authentication to use this service because we would like to keep it as simple as possible. Please do not abuse the service or you will force us to require a registration (subject to approval) to continue using it.
