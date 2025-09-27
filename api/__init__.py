from fastapi import APIRouter
from api.v1.routers import health
from api.v1.routers import users

api_router = APIRouter()

# Include all routers
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(users.router)