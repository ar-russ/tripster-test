# pylint: disable=invalid-name

from enum import Enum


class VoteType(str, Enum):
    upvote = "upvote"
    downvote = "downvote"

    @classmethod
    def values(cls) -> list[str]:
        """
        Получение значений всех членов Enum в качестве списка
        :return: Список значений
        """
        return list(map(lambda member: member.value, cls))
