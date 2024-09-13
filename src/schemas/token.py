from pydantic import BaseModel

from src.schemas.base_response import BaseResponse


class TokenInfo(BaseModel):
    access_token: str
    token_type: str = "Bearer"


class TokenInfoResponse(BaseResponse):
    payload: TokenInfo
