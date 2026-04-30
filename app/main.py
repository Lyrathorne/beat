from fastapi import FastAPI

from app.database import Base, engine
from app.routers.users import router as users_router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Beat API")

app.include_router(users_router)


@app.get("/")
def root():
    return {"message": "Beat backend is running"}