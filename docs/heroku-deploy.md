# Deploying to heroku

## Setup

[Login to the heroku command line interface as described here](https://devcenter.heroku.com/articles/getting-started-with-python#set-up).

## Create the app in heroku

```
heroku apps:create NAME_OF_APP
```

## Uvicorn configuration

[In production](https://www.uvicorn.org/deployment/) we run uvicorn via gunicorn with
`gunicorn -k uvicorn.workers.UvicornWorker`.

[Heroku recommends](https://devcenter.heroku.com/articles/python-gunicorn) controlling the concurrency with the `WEB_CONCURRENCY` environment variable:

```
heroku config:set WEB_CONCURRENCY=3
```

## Create a database
```
heroku addons:create heroku-postgresql:hobby-dev
```

## Deploy code
```
git push heroku master
```

## Ensure at least one instance is running

```
heroku ps:scale web=1
```

Check the application is running with:

```
heroku open
```

## Import the data

```
heroku run python covidapi/import_data.py
```
