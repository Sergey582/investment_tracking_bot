from app.api.public.modules.users.serializers import RegisterUserRequest, HostSetRequest
from app.core.modules.users.services import create_user
from fastapi import APIRouter
from starlette import status
from starlette.responses import Response
import os

router = APIRouter()


@router.post(
    "/registration",
    tags=["user"],
    summary="Register a new user",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def router_create_user(request_data: RegisterUserRequest):
    await create_user(
        user_id=request_data.user_id,
        username=request_data.username,
    )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.post(
    "/host",
    tags=["user"],
    summary="set host",
    status_code=status.HTTP_204_NO_CONTENT,
)
async def router_create_user(request_data: HostSetRequest):
    os.environ["host"] = request_data.host
    r = Response(status_code=status.HTTP_204_NO_CONTENT)
    r.headers["Access-Control-Allow-Origin"] = os.environ["host"]
    return r
