from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from schemas import UserCreate, UserRead
from models import User
from db import get_db
from utils.auth_utils import hash_password, verify_password
from utils.token_utils import create_access_token

router = APIRouter(prefix="/v1/auth")
OAuth2_scheme = OAuth2PasswordBearer(tokenUrl="/v1/auth/login")

@router.post("/register", response_model=UserRead)
async def register(cred: UserCreate, db: AsyncSession = Depends(get_db)):
    response = await db.execute(select(User).where(User.email == cred.email))
    existing_user = response.scalar_one_or_none()

    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = hash_password(cred.password)
    new_user = User(
        email = cred.email,
        username = cred.username,
        hashed_pwd = hashed_password,
        avatar = cred.avatar,
        bio = cred.bio
    )

    db.add(new_user)
    await db.commit()
    await db.refresh(new_user)

    return new_user

@router.post("/login")
async def login(data: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    response = await db.execute(select(User).where(User.email == data.username))
    existing_user = response.scalar_one_or_none()

    if not existing_user or not verify_password(data.password, existing_user.hashed_pwd):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token = create_access_token(data={"sub":str(existing_user.user_id)})
    return {"access_token": access_token, "token_type": "bearer"}