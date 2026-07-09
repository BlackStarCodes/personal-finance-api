from fastapi import FastAPI
from .routers import users, auth, wallets


app = FastAPI()


app.include_router(users.router, tags=['users'], prefix="/users")
app.include_router(auth.router, tags=['auth'], prefix="/auth")
app.include_router(wallets.router, tags=['wallets'], prefix='/wallets')