from fastapi import APIRouter
from  routes.devops.ping.routes.index import router as ping_router
router = APIRouter()

router.include_router(ping_router, prefix='/devop')