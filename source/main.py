from fastapi import FastAPI
from source.routers import users, auth, wallets, categories, transactions


app = FastAPI()


app.include_router(users.router, tags=['users'], prefix="/users")
app.include_router(auth.router, tags=['auth'], prefix="/auth")
app.include_router(wallets.router, tags=['wallets'], prefix='/wallets')
app.include_router(categories.router, tags=['categories'], prefix='/categories')
app.include_router(transactions.router, tags=['transactions'], prefix='/transactions')