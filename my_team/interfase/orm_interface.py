import typing
from abc import abstractmethod, ABC, abstractstaticmethod
from sqlalchemy.ext.asyncio import AsyncSession as Session
from sqlalchemy import select, Table
from fastapi import HTTPException


class OrmInterface:
    @abstractmethod
    async def create_record(self, db: Session, data: typing.Any, where: typing.Optional, message: str):
        raise NotImplementedError

    @abstractmethod
    async def view_record(self, db: Session, data: typing.Any, where: typing.Optional):
        raise NotImplementedError

    @abstractmethod
    async def delete_record(self, db: Session, data: typing.Any, where: typing.Optional):
        raise NotImplementedError

    @abstractmethod
    async def be_current_record(self, db: Session, data: typing.Any, where: typing.Optional):
        raise NotImplementedError

    @abstractmethod
    async def get_current_user(self, db: Session,
                               where: typing.Optional,
                               message: str):
        raise NotImplementedError

    @abstractmethod
    async def _get_record_orm(self, db: Session, value: typing.Any):
        raise NotImplementedError

    @abstractmethod
    async def create_foreign_record(self, db: Session, first_model: Table,
                                    second_model: Table, data: typing.Any):
        raise NotImplementedError


class ORM(OrmInterface, ABC):
    def __init__(self, value):
        self.__classDB = value

    async def create_record(self, db: Session, data: typing.Any,
                            where: typing.Optional, message=''):
        if await self._be_current_record(db, where=where):
            record = self.__classDB(**data.dict())
            db.add(record)
            await db.commit()
            await db.refresh(record)
            return record
        else:
            raise HTTPException(
                status_code=400,
                detail=message
            )

    async def delete_record(self, db: Session, data: typing.Any, where: typing.Optional):
        record = db.query(self.__classDB).filter(where).first()
        return record

    async def view_record(self, db: Session, data: typing.Any, where: typing.Optional):
        record = (db.query(self.__classDB)
                  .filter(where)
                  .first())
        return record

    async def _be_current_record(self, db: Session, where: typing.Optional):
        record = select(self.__classDB).where(where)
        result = await db.execute(record)
        if result.scalar() is not None:
            return False
        return True

    async def get_current_user(self, db: Session, where: typing.Optional, message: str = ''):
        record = select(self.__classDB).where(where)
        result = await self._get_record_orm(db, record)
        if result is not None:
            return result
        else:
            raise HTTPException(
                status_code=404,
                detail=message
            )

    async def _get_record_orm(self, db: Session, value: typing.Any):
        result = await db.execute(value)
        return result.unique().scalar_one_or_none()


