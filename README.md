# covid-api
COVID19 Api based on Johns Hopkins CSSE data

The intent of this project is to create an API which will make easier to access the COVID19 reports provided by the Johns Hopkins CSSE: https://github.com/CSSEGISandData/COVID-19

# Status

We are in the early phase of the project and framework, architectural and other decisions haven't been taken yet. Please help discussing them in the GitHub **Issues** section of this project.

# Project setup
First, create a virtualenv, activate it, and then install the dependencies:

```
python -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

Then run the app with:

```
uvicorn covidapi.app:app --reload
```

The API will be served at [http://localhost:8000/](http://localhost:8000/)

The API docs are served at [http://localhost:8000/docs](http://localhost:8000/docs)