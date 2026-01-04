from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.api import deps
from app.models.user import User
from app.schemas.user import UserRead, UserUpdate, UserPasswordChange
from app.services import user_service
from app.core import security

router = APIRouter()

@router.get("/me", response_model=UserRead)
async def read_user_me(
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    return current_user

@router.patch("/me", response_model=UserRead)
async def update_user_me(
    *,
    db: AsyncSession = Depends(deps.get_db),
    user_in: UserUpdate,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    user = await user_service.update(db, db_obj=current_user, obj_in=user_in)
    return user

@router.put("/me/password", response_model=UserRead)
async def change_password_me(
    *,
    db: AsyncSession = Depends(deps.get_db),
    password_in: UserPasswordChange,
    current_user: User = Depends(deps.get_current_user),
) -> Any:
    if not security.verify_password(password_in.current_password, current_user.password_hash):
        raise HTTPException(status_code=400, detail="Incorrect password")
    
    user_in = UserUpdate(password=password_in.new_password)
    user = await user_service.update(db, db_obj=current_user, obj_in=user_in)
    return user
