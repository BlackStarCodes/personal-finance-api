from fastapi import FastAPI
from .routers import users, auth


app = FastAPI()


app.include_router(users.router, prefix="/users")
app.include_router(auth.router, prefix="/auth")