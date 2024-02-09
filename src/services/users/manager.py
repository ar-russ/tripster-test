from fastapi import Depends
from fastapi_users import BaseUserManager, IntegerIDMixin

from src.models.db.user import User
from src.services.db.users import user_service


class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    pass


async def get_user_manager(user_db=Depends(user_service.get_user_db)):
    """
    Фактори менеджера для работы с пользователями
    """
    yield UserManager(user_db)
