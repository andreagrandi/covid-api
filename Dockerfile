FROM python:3
WORKDIR /covidapi
COPY requirements.txt requirements-test.txt /covidapi/
RUN pip install -r /covidapi/requirements.txt -r /covidapi/requirements-test.txt

CMD ["uvicorn", "covidapi.app:app", "--host", "0.0.0.0", "--reload"]
