import logging
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from schemas.user import UserCreate, UserRead
from services.users import UserService
from settings.db import get_db
from utils.security import verify_password, security

logger = logging.getLogger(__name__)
router = APIRouter(tags=["Authentication"])


@router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def register(user_data: UserCreate, db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    existing_user = await user_service.get_by_email(user_data.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )
    # Першого користувача можна зробити admin, або передати 'user'
    return await user_service.create_user(email=user_data.email, password=user_data.password, role="user")


@router.post("/login")
async def login(credentials: OAuth2PasswordRequestForm = Depends(), db: AsyncSession = Depends(get_db)):
    user_service = UserService(db)
    user = await user_service.get_by_email(credentials.username)  # OAuth2 форма передає email у поле username

    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password"
        )

    # Генеруємо JWT токен. Записуємо роль в payload (id користувача в sub, роль у custom_claims)
    access_token = security.create_access_token(
        uid=str(user.id),
        fresh=True,
        custom_claims={"role": user.role}
    )
    return {"access_token": access_token, "token_type": "bearer"}