from fastapi import FastAPI
from .api import views

foo = 'bar'
app = FastAPI()
app.include_router(views.router)
