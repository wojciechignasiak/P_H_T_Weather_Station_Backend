from fastapi import APIRouter
from router import enpoints

api_router = APIRouter()
api_router.include_router(enpoints.router)
