from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from interfase.orm_interface import ORM
from users.models import users_model
from sqlalchemy.ext.asyncio import AsyncSession as Session
from users import shemas
from users.depends import pars_dota_match
from config import get_async_session

users_router = APIRouter(
    tags=['users'],
    prefix='/users',
)


@users_router.post("/auth")
async def users_auth(users: shemas.User, db: Session = Depends(get_async_session)):
    user = ORM(users_model.User)
    return await user.create_record(db, users, message="Пользователь существует",
                                    where=(users_model.User.email == users.email))


@users_router.get("/profile/{email}")
async def profile_user(email: str, db: Session = Depends(get_async_session)):
    user = ORM(users_model.User)
    return await user.get_current_user(db, email, message='Пользователя нет',
                                       where=(users_model.User.email == email))


@users_router.post("/create-dota-user")
async def dota_user(profile: shemas.DotaProfileCreate,
                    backgroundTask: BackgroundTasks,
                    db: Session = Depends(get_async_session)):
    orm = ORM(users_model.User)
    user = await orm.get_current_user(db, message='Пользователя нет',
                                       where=(users_model.User.email == profile.email.email))
    await users_model.DotaProfileUser().create_user(db, user=user, data=profile.account_id)
    backgroundTask.add_task(pars_dota_match.get_matches, profile.account_id.account_id)
    return user


