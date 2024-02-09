from fastapi_users import FastAPIUsers
from fastapi_users.authentication import AuthenticationBackend, BearerTransport, JWTStrategy

from src.services.users.manager import get_user_manager
from src.models.db.user import User
from config.config import settings

bearer_transport = BearerTransport(tokenUrl="login")


def get_jwt_strategy() -> JWTStrategy:
    """
    Фактори стратегии аутентификации для последующей
    конфигурации работы всей аутентификации в сервисе
    """
    return JWTStrategy(secret=settings.AUTH.SECRET, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)

user_auth = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)


def get_current_user():
    """
    Получение текущего пользователя в рамках запроса к ручке,
    используется в качестве зависимости FastAPI
    """
    return user_auth.current_user()
