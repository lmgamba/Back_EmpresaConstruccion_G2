from fastapi import FastAPI
from routes import auth_routes, user_routes

#levantar el servidor

app = FastAPI()

app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])