from fastapi import APIRouter
from models import User, db
from slqalchemy.orm import sessionmaker

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

# create user - logic form
'''
@auth_router.post("/create_account")
async def create_account(email: str, password: str, name: str):
    Session = sessionmaker(bind=db)
    session = Session()
    user = session.query(User).filter(User.email==email).first()
    if user:
        return {"message": "User already exist with this email"}
    else:
        new_user = User(name, email,password)
        session.add(new_user)
        session.commit()
        return {"message": "User successfully registered"}
'''

