from fastapi import FastAPI
from .api import views
from starlette.staticfiles import StaticFiles
from pathlib import Path

current_file = Path(__file__)
parent_dir = current_file.parent
static_dir = f"{parent_dir.resolve()}/api/static"

app = FastAPI()
app.mount("/index.html", StaticFiles(directory=static_dir), name="static")
app.include_router(views.router)