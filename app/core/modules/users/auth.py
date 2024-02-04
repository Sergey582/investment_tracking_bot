import hashlib
import hmac
from urllib.parse import parse_qs

from app.core.config import BOT_TOKEN
from app.core.modules.assets.models import User
from fastapi import Depends, HTTPException
from pydantic import BaseModel
from starlette import status
from starlette.requests import Request


class Credentials(BaseModel):
    data_check_string: str
    received_hash: str
    telegram_user_id: int


class AuthenticationFailed(HTTPException):

    def __init__(self, detail=None):
        status_code = status.HTTP_401_UNAUTHORIZED
        super().__init__(status_code=status_code, detail=detail)


def calculate_hmac_sha256_signature(bot_token):
    # The secret key is "WebAppData"
    secret_key = "WebAppData"

    # Convert the secret key and bot token to bytes
    secret_key_bytes = secret_key.encode('utf-8')
    bot_token_bytes = bot_token.encode('utf-8')

    # Calculate the HMAC-SHA-256 signature
    hmac_signature = hmac.new(secret_key_bytes, bot_token_bytes, hashlib.sha256)

    # Get the hexadecimal representation of the signature
    signature_hex = hmac_signature.hexdigest()

    return hmac_signature


def verify_telegram_data(initial_data: str) -> bool:
    parsed_data = parse_qs(initial_data)
    received_hash = parsed_data.pop('hash')[0]
    data_check_string = '\n'.join([f"{key}={parsed_data[key][0]}" for key in sorted(parsed_data.keys())])

    secret_key = calculate_hmac_sha256_signature(BOT_TOKEN)
    message = data_check_string.encode('utf-8')
    generated_hash = hmac.new(secret_key.digest(), message, hashlib.sha256).hexdigest()
    return generated_hash == received_hash


async def user_auth_check(request: Request, credentials: Credentials = Depends()) -> User:
    # if not credentials:
    #     raise AuthenticationFailed
    #
    # if not verify_telegram_data(initial_data=credentials.data_check_string):
    #     raise AuthenticationFailed("invalid credentials")

    user_id = credentials.telegram_user_id
    user = await User.filter(user_id=user_id).first()

    if user is None:
        user = User(user_id=user_id)
        await user.save()

    return user
