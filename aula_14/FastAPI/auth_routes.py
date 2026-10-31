from fastapi import APIRouter, Depends, HTTPException
from models import User
from dependencies import get_session
from main import bcrypt_context

auth_router = APIRouter(prefix="/auth", tags=["auth"])

@auth_router.get("/")
async def home():
    """
    Default system route.
    """
    return {
        "message": "System's default path",
        "authenticate": False
            }

# create user
@auth_router.post("/create_account")
async def create_account(email: str, password: str, name: str, session=Depends(get_session)):
    user = session.query(User).filter(User.email == email).first()

    if user:
        return {"message": "User already exist with this email"}

    if len(password.encode("utf-8")) > 72:
        return {"message": "Password must have a maximum of 72 bytes"}

    password_crypt = bcrypt_context.hash(password)

    new_user = User(name, email, password_crypt)
    session.add(new_user)
    session.commit()

    return {"message": "User successfully registered"}
