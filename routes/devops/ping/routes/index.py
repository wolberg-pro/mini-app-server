
from fastapi.routing import APIRouter
from starlette import status
from starlette.responses import JSONResponse

router = APIRouter()


@router.get('/')
def health_check():
    return JSONResponse({ "status":"pass"},status_code=status.HTTP_200_OK)