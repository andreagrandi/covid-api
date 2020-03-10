from fastapi import FastAPI
from .api import views
from .db.database import Base, engine

# FIXME: where should this live? This creates the schema, but we don't need it if just running the tests.
Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(views.router)
