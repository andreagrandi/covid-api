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

# Exposure notification API modes

Exposure Notifications API modesIn v1.5 and higher, the Exposure Notifications API introduced ExposureWindow mode to provide enhanced risk calculation functionality.
We strongly recommend migrating to ExposureWindow mode. This mode allows you to separately view and revise or revoke matches from multiple days, while still leaving enough quota to update six times per day. Although the legacy v1 mode has more quota that can be used to partition matches by day, your app wastes the user's battery to do so and can even sometimes run out of quota.Alert: When ExposureWindow mode was introduced in v1.5, we began referring to legacy v1 functionality as v1 mode (or the legacy v1 mode). The API continues to maintain support for legacy v1 mode to avoid breakage of apps that use legacy features. However, we strongly recommend against using the legacy v1 mode, especially if you're developing a new app.

1)Select the mode based on the provideDiagnosisKeys method used:

2)To enable the ExposureWindow feature (thereby deactivating the ExposureSummary and ExposureInformation features), call provideDiagnosisKeys(files) with only the list of files.

3)To enable the ExposureSummary and ExposureInformation features (thereby deactivating the ExposureWindow feature), call provideDiagnosisKeys(files, token, config) with a token.

4)The API is backward compatible with all versions: it activates non-breaking changes when a new version is available on the device, even when using the legacy v1 mode. Such changes would include, for example, the same-day release of keys and the ability to provide keys from multiple files with different signatures in one call.

# Disclaimer

We are doing our best to keep the available data updated, clean (removing duplicates), and to provide a reliable service, but we are not in any way responsible for the accuracy of the data nor for the availability of the service itself. Please **use it at your own risk**.

**Abuse notice:** we are currently not requiring any registration or authentication to use this service because we would like to keep it as simple as possible. Please do not abuse the service or you will force us to require a registration (subject to approval) to continue using it.
