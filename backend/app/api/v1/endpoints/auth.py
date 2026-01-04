from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.core import security
from app.schemas.user import Token, UserCreate, UserRead
from app.services import user_service

router = APIRouter()

@router.post("/login", response_model=Token)
async def login(
    db: AsyncSession = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    # 디버그 (DEBUG)
    print(f"DEBUG: db session type: {type(db)}")
    
    user = await user_service.get_by_email(db, email=form_data.username)
    
    # 디버그 (DEBUG)
    print(f"DEBUG: user type: {type(user)}")
    if user:
        print(f"DEBUG: user repr: {user}")
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    
    # 안전한 접근 (Safe access)
    if isinstance(user, dict):
        password_hash = user.get("password_hash")
        user_id = user.get("id")
        is_active = user.get("is_active")
    else:
        password_hash = user.password_hash
        user_id = user.id
        is_active = user.is_active

    if not security.verify_password(form_data.password, password_hash):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect email or password",
        )
    elif not is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    
    access_token = security.create_access_token(subject=user_id)
    return {
        "access_token": access_token,
        "token_type": "bearer",
    }

@router.post("/signup", response_model=UserRead)
async def signup(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserCreate,
) -> Any:
    user = await user_service.get_by_email(db, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this email already exists in the system.",
        )
    user = await user_service.create(db, obj_in=user_in)
    return user
