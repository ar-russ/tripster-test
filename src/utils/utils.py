from src.models.db import Post
from src.models.dto.post import GetPost
from src.services.db.rating import rating_service


async def get_post_view(post: Post) -> GetPost:
    """
    Получение DTO из БД инстанса публикации
    :param post: Объект публикации из ORM
    :return: Pydantic-Модель GetPost, содержащая информацию
    о публикации которую нужно выводить в ответах API
    """
    return GetPost(
        body=post.body,
        created=post.created,
        author_id=post.author_id,
        votes_amount=len(await rating_service.get_post_votes(post.id)),
        rating=await rating_service.get_post_rating(post.id),
    )
