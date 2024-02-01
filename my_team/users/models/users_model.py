from sqlalchemy import Integer, ForeignKey, String, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from fastapi_users.db import SQLAlchemyBaseUserTable, SQLAlchemyUserDatabase
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from config import get_async_session

Base = declarative_base()


class Role(Base):
    __tablename__ = 'role'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    #permissions = Column()


class User(SQLAlchemyBaseUserTable[int], Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True)
    dota_profile_user = relationship("DotaProfileUser", back_populates='user_id')
    role = Column(Integer, ForeignKey('role.id'))


class DotaProfileUser(Base):
    __tablename__ = "dota_profile_user"

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer)

    user = Column(Integer, ForeignKey('user.id'))
    user_id = relationship("User", back_populates='dota_profile_user')

    @staticmethod
    async def create_user(db: AsyncSession, user, data):
        data = DotaProfileUser(**data.dict(), user=user.id)
        db.add(data)
        await db.commit()
        await db.refresh(data)
        return data


async def get_user_db(session: AsyncSession = Depends(get_async_session)):
    yield SQLAlchemyUserDatabase(session, User)