from sqlalchemy import desc
from sqlalchemy.sql import func
from sqlalchemy.future import select

from src.services.db.base import BaseDBService
from src.services.db.rating import rating_service
from src.models.db import Post, User, Vote
from src.enums.rating import VoteType


class PostsService(BaseDBService):
    async def get(self, post_id: int) -> Post:
        """
        Получение БД объекта публикации по её ID
        :param post_id: ID публикации в БД
        :return: Объект Post, содержащий информацию о публикации
        """
        statement = select(Post).where(Post.id == post_id)

        result = await self.session.execute(statement)
        return result.scalar_one()

    async def create(
            self,
            body: int,
            author: User
    ) -> Post:
        """
        Создание новой публикации
        :param body: Текст публикации
        :param author: БД-объект автора публикации
        """

        # Мёрджим объект автора в текущую сессию во избежании конфликтов
        author = await self.session.merge(author)
        post = Post(
            body=body,
            author_id=author.id,
            author=author,
        )
        self.session.add(post)
        await self.session.commit()
        return post

    async def get_latest_posts(self, amount: int) -> list[Post]:
        """
        Получение публикаций, отфильтрованных по дате создания, начиная с самой последней
        :param amount: Кол-во публикаций для вывода
        :return: Список БД-объектов Post
        """
        statement = select(Post).order_by(desc(Post.created)).limit(amount)
        result = await self.session.execute(statement)
        return list(result.scalars())

    async def get_best_posts(self, amount: int) -> list[Post]:
        """
        Получение публикаций, отфильтрованных по рейтингу, начиная с самой лучшей
        :param amount: Кол-во публикаций для вывода
        :return: Список БД-объектов Post
        """
        upvotes_count = (select(func.count())
                         .where(Vote.post_id == Post.id)
                         .where(Vote.type == VoteType.upvote).scalar_subquery())
        downvotes_count = (select(func.count())
                           .where(Vote.post_id == Post.id)
                           .where(Vote.type == VoteType.downvote).scalar_subquery())

        statement = select(Post).order_by(desc(upvotes_count - downvotes_count)).limit(amount)
        result = await self.session.execute(statement)
        return list(result.scalars())

    @staticmethod
    async def upvote(post_id: int, user_id: int) -> None:
        """
        Присвоение посту оценки upvote
        :param post_id: ID публикации, которую нужно оценить
        :param user_id: ID пользователя, поставившего оценку
        """
        await rating_service.create_vote(user_id, post_id, VoteType.upvote)

    @staticmethod
    async def downvote(post_id: int, user_id: int) -> None:
        """
        Присвоение посту оценки upvote
        :param post_id: ID публикации, которую нужно оценить
        :param user_id: ID пользователя, поставившего оценку
        """
        await rating_service.create_vote(user_id, post_id, VoteType.downvote)


posts_service = PostsService()
