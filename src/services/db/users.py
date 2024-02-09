from fastapi import Depends
from fastapi_users.db import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.db import User
from src.services.db.base import BaseDBService


class UserService(BaseDBService):

    @staticmethod
    async def get_user_db(session: AsyncSession = Depends(BaseDBService.get_async_session)):
        """
        Фактори адаптера базы данных для работы с пользователями
        """
        yield SQLAlchemyUserDatabase(session, User)


user_service = UserService()
