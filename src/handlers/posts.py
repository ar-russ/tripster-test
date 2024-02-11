# pylint: disable=missing-function-docstring

from fastapi import APIRouter, HTTPException, Depends

from src.enums.rating import VoteType
from src.enums.filters import Filter
from src.models.db import User
from src.models.dto.post import CreatePost, GetPost
from src.services.db.posts import posts_service
from src.services.db.rating import rating_service
from src.services.users.auth import get_current_user
from src.utils.utils import get_post_view

router = APIRouter()


@router.get("/post/{post_id}")
async def get_post(post_id: int) -> GetPost:
    post = await posts_service.get(post_id)
    if not post:
        raise HTTPException(404, detail="Post not found")

    return await get_post_view(post)


@router.post("/post")
async def create_post(post_data: CreatePost, user: User = Depends(get_current_user())) -> int:

    post = await posts_service.create(post_data.body, user)
    return post.id


@router.post("/post/{post_id}/upvote")
async def upvote_post(post_id: int, user: User = Depends(get_current_user())):
    if not await posts_service.get(post_id):
        raise HTTPException(404, detail="Post not found")

    if not await rating_service.is_post_voted_by_user(post_id, user.id):
        await posts_service.upvote(post_id, user.id)
        return {"success": True}

    user_vote = await rating_service.get_user_post_vote(post_id, user.id)
    if user_vote.type == VoteType.upvote:
        raise HTTPException(400, detail="You already upvoted this post")

    await rating_service.cancel_user_vote(post_id, user.id)
    await posts_service.upvote(post_id, user.id)
    return {"success": True}


@router.post("/post/{post_id}/downvote")
async def downvote_post(post_id: int, user: User = Depends(get_current_user())):
    if not await posts_service.get(post_id):
        raise HTTPException(404, detail="Post not found")

    if not await rating_service.is_post_voted_by_user(post_id, user.id):
        await posts_service.downvote(post_id, user.id)
        return {"success": True}

    user_vote = await rating_service.get_user_post_vote(post_id, user.id)
    if user_vote.type == VoteType.downvote:
        raise HTTPException(400, detail="You already downvoted this post")

    await rating_service.cancel_user_vote(post_id, user.id)
    await posts_service.downvote(post_id, user.id)
    return {"success": True}


@router.post("/post/{post_id}/cancel-vote")
async def cancel_vote(post_id: int, user: User = Depends(get_current_user())):
    if not await posts_service.get(post_id):
        raise HTTPException(404, detail="Post not found")

    if not await rating_service.is_post_voted_by_user(post_id, user.id):
        raise HTTPException(400, detail="You didn't vote for this post")

    await rating_service.cancel_user_vote(post_id, user.id)
    return {"success": True}


@router.get("/posts")
async def get_posts(sorting: Filter, amount: int = 10) -> list[GetPost]:
    if sorting == Filter.latest:
        return await posts_service.get_latest_posts(amount)
    if sorting == Filter.best:
        return await posts_service.get_best_posts(amount)
