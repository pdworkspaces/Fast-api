from fastapi import FastAPI
from app.routes.user_routes import router as user_router
from app.auth.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)
app.include_router(user_router)