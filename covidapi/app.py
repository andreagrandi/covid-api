from fastapi import FastAPI
from .api import views

app = FastAPI()
app.include_router(views.router)
