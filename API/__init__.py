from fastapi import APIRouter

from API.api_v1.users.views import router as users_router


router = APIRouter()
router.include_router(
    users_router
)
