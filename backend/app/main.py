from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from jose import JWTError

from app.auth import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token,
    ACCESS_TOKEN_EXPIRE_SECONDS,
)
from app.models import Token, TokenRefresh, RefreshRequest

app = FastAPI(
    title="JWT Authentication API",
    description="FastAPI application implementing JWT authentication",
    version="0.1.0",
)


@app.post("/token", response_model=Token, summary="Obtain JWT tokens")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Authenticate with username and password to receive access and refresh tokens.

    - **username**: admin
    - **password**: admin123

    The access token expires in **300 seconds**.
    """
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token = create_access_token(data={"sub": user["username"]})
    refresh_token = create_refresh_token(data={"sub": user["username"]})
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
    )


@app.post("/token/refresh", response_model=TokenRefresh, summary="Refresh access token")
async def refresh_token(request: RefreshRequest):
    """
    Use a valid refresh token to obtain a new access token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid or expired refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = decode_token(request.refresh_token)
        if payload.get("type") != "refresh":
            raise credentials_exception
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    new_access_token = create_access_token(data={"sub": username})
    return TokenRefresh(
        access_token=new_access_token,
        token_type="bearer",
        expires_in=ACCESS_TOKEN_EXPIRE_SECONDS,
    )


@app.get("/health", summary="Health check")
async def health_check():
    return {"status": "ok"}
