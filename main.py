from fastapi import FastAPI
import uvicorn

from config.config import settings
from src.handlers.posts import router as posts_router
from src.services.users.auth import user_auth, auth_backend
from src.models.dto.user import GetUser, CreateUser


def build_app() -> FastAPI:
    """
    Конфигурация FastAPI приложения
    """
    app = FastAPI()

    app.include_router(posts_router)
    app.include_router(user_auth.get_auth_router(auth_backend))
    app.include_router(user_auth.get_register_router(GetUser, CreateUser))

    return app


if __name__ == "__main__":
    server = uvicorn.Server(
        uvicorn.Config(
            app=build_app(),
            host=settings.HOST,
            port=settings.PORT,
        )
    )
    server.run()
