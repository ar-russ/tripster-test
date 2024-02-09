from typing import Optional

from sqlalchemy.future import select

from src.services.db.base import BaseDBService
from src.models.db import Vote
from src.enums.rating import VoteType


class RatingService(BaseDBService):
    async def create_vote(self, user_id: int, post_id: int, vote_type: VoteType) -> None:
        """
        Создание оценки в БД
        :param user_id: ID пользователя, поставившего оценку
        :param post_id: ID публикации, на которую поставлена оценка
        :param vote_type: Тип оценки (upvote/downvote)
        """
        vote = Vote(
            user_id=user_id,
            post_id=post_id,
            type=vote_type,
        )
        self.session.add(vote)
        await self.session.commit()

    async def is_post_voted_by_user(self, post_id: int, user_id: int) -> bool:
        """
        Проверка на то, оценивал ли пользователь публикацию
        :param post_id: ID публикации, которую нужно проверить
        :param user_id: ID пользователя, который мог поставить оценку
        :return: True/False
        """
        vote = await self.get_user_post_vote(post_id, user_id)
        return vote is not None

    async def cancel_user_vote(self, post_id: int, user_id: int) -> None:
        """
        Отмена оценки пользователя на конкретной публикации
        :param post_id: ID публикации, на которую была поставлена оценка
        :param user_id: ID пользователя, который поставил оценку
        """
        if not await self.is_post_voted_by_user(post_id, user_id):
            return

        vote = await self.get_user_post_vote(post_id, user_id)
        await self.session.delete(vote)
        await self.session.commit()

    async def get_user_post_vote(self, post_id: int, user_id: int) -> Optional[Vote]:
        """
        Получение БД объекта оценки пользователя на конкретной публикации
        :param post_id: ID публикации, из которой нужно получить оценку
        :param user_id: ID пользователя, который поставил оценку
        :return: БД-объект оценки либо None, если пользователь не оценивал указанную публикацию
        """
        statement = select(Vote).where(Vote.post_id == post_id).where(Vote.user_id == user_id)
        result = await self.session.execute(statement)

        result = result.scalar()
        if not result:
            return
        return result

    async def get_post_votes(self, post_id: int) -> list[Vote]:
        """
        Получить все оценки на конкретной публикации
        :param post_id: ID публикации, оценки которой нужно получить
        :return: Список БД-объектов оценок
        """
        statement = select(Vote).where(Vote.post_id == post_id)
        result = await self.session.execute(statement)
        return list(result.scalars())

    async def get_post_rating(self, post_id: int) -> int:
        """
        Расчёт рейтинга конкретной публикации. Рейтинг высчитывается по формуле:
        upvotes - downvotes
        :param post_id: ID публикации, рейтинг которой нужно посчитать
        :return: Рейтинг публикации в целочисленном формате
        """
        votes = await self.get_post_votes(post_id)

        upvotes = [vote for vote in votes if vote.type == VoteType.upvote]
        downvotes = [vote for vote in votes if vote.type == VoteType.downvote]

        return len(upvotes) - len(downvotes)


rating_service = RatingService()
