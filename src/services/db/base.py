from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker

from config.config import settings

engine = create_async_engine(
    url=settings.POSTGRES.build_url(),
)
session_factory = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False,
)


class BaseDBService:
    def __init__(self):
        self.session: AsyncSession = session_factory()

    @staticmethod
    async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
        """
        Фактори асинхронной сессии базы данных
        :return:
        """
        async with session_factory() as session:
            yield session
