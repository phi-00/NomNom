from fastapi import APIRouter

router = APIRouter()

from .auth import router as auth_router
from .accounts import router as accounts_router

router.include_router(auth_router, prefix="/auth", tags=["auth"])
router.include_router(accounts_router, prefix="/accounts", tags=["accounts"])