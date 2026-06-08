from pydantic import BaseModel
from typing import Optional


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str
    expires_in: int


class TokenRefresh(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


class RefreshRequest(BaseModel):
    refresh_token: str
