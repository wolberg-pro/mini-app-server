from fastapi import APIRouter
from routes.devops.ping.tests import test_ping

router = APIRouter()

router.include_router(test_ping, prefix='/health-check')