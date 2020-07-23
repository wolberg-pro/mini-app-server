from fastapi import APIRouter
from routes.devops.routes import router as devops_router
router = APIRouter()

router.include_router(devops_router, prefix='/api/v1', tags=['devops'])