from fastapi import FastAPI
from routes import assignments_routes, auth_routes, user_routes, constructions_routes, logs_routes
from fastapi.middleware.cors import CORSMiddleware

#levantar el servidor

app = FastAPI()

# cors middleware
app.add_middleware( CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"], )


app.include_router(auth_routes.router, prefix="/auth", tags=["Auth"])
app.include_router(user_routes.router, prefix="/users", tags=["Users"])
app.include_router(constructions_routes.router, prefix="/constructions", tags=["Constructions"])
app.include_router(assignments_routes.router, prefix="/assignments", tags=["Assignments"])
app.include_router(logs_routes.router, prefix="/logs", tags=["Logs"])