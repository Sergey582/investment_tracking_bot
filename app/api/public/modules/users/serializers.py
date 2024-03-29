from pydantic import BaseModel


class RegisterUserRequest(BaseModel):
    user_id: int
    username: str


class HostSetRequest(BaseModel):
    host: str
