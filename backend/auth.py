from fastapi import APIRouter, Request, Depends
from sqlalchemy.orm import Session
from starlette.responses import RedirectResponse
from authlib.integrations.starlette_client import OAuth
from jose import jwt
from dotenv import load_dotenv
import os

from models import User, RoleEnum
from database import get_db

load_dotenv()
router = APIRouter()

SECRET_KEY = os.getenv("SECRET_KEY")
FRONTEND_REDIRECT_URL = os.getenv("FRONTEND_REDIRECT_URL", "http://localhost:3000/oauth-success")

oauth = OAuth()
oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile"}
)

def create_token(data: dict):
    return jwt.encode(data, SECRET_KEY, algorithm="HS256")


@router.get("/auth/login")
async def login(request: Request):
    redirect_uri = request.url_for('auth_callback')
    return await oauth.google.authorize_redirect(request, redirect_uri)


@router.get("/auth/callback")
async def auth_callback(request: Request, db: Session = Depends(get_db)):
    token = await oauth.google.authorize_access_token(request)
    user_info = token.get("userinfo")

    if not user_info:
        return {"error": "Failed to retrieve user info"}

    email = user_info["email"]
    user = db.query(User).filter(User.email == email).first()

    if not user:
        user = User(email=email, hashed_password="", role=RoleEnum.REPORTER)
        db.add(user)
        db.commit()
        db.refresh(user)

    jwt_token = create_token({"sub": user.email, "id": user.id, "role": user.role})
    response = RedirectResponse(url=f"{FRONTEND_REDIRECT_URL}?token={jwt_token}")
    return response
