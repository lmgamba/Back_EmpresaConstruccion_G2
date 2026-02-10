from fastapi import FastAPI
from routes import auth_routes

#levantar el servidor

app = FastAPI()

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])