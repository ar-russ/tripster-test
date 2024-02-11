# pylint: disable=invalid-name

from src.enums.base import ExtendedEnum


class VoteType(str, ExtendedEnum):
    upvote = "upvote"
    downvote = "downvote"
