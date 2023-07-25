from datetime import datetime
from typing import Dict, List, Optional
from uuid import UUID

from pydantic import Field, root_validator, validator

from models.base import APIResponse, OrjsonMixin, VotesChoices


class BookmarkResponse(APIResponse):
    """Модель ответа для представления закладки (отложенный на потом фильм)."""

    film_id: UUID


class Vote(OrjsonMixin):
    """Класс пользовательской оценки."""

    user_id: UUID
    score: VotesChoices


class RatingResponse(APIResponse):
    """Модель ответа для представления рейтинга."""

    likes: int = Field(default=0)
    dislikes: int = Field(default=0)
    average_rating: Optional[int]
    votes: Optional[List[Vote]] = Field(exclude=True)

    @root_validator
    def scoring(cls, data: Dict) -> Dict:
        """Основной валидатор для подсчета количества лайков, дизлайков и средней пользовательской оценки.

        Args:
            data: Данные с голосами пользователей

        Returns:
            Dict: Подсчитанный рейтинг
        """
        if votes := data.get('votes'):
            total_scores = 0
            for vote in votes:
                if vote.score == VotesChoices.like.value:
                    data['likes'] += 1
                elif vote.score == VotesChoices.dislike.value:
                    data['dislikes'] += 1
                total_scores += vote.score
            data['average_rating'] = total_scores // (data['likes'] + data['dislikes'])
        return data


class ReviewResponse(APIResponse):
    """Модель ответа для представления рецензии на фильм."""

    id: UUID = Field(alias='_id')
    author: UUID
    film_id: UUID
    text: str
    pub_date: datetime
    film_score: Optional[VotesChoices]
    likes: int = Field(default=0)
    dislikes: int = Field(default=0)
    average_rating: Optional[int]

    @validator('film_score')
    def get_film_vote(cls, film_score: VotesChoices) -> str:
        """Валидация оценки фильма автором рецензии для приведения её в лайк или дизлайк.

        Args:
            film_score: Оценка фильма, привязанная к рецензии

        Returns:
            str: Лайк или дизлайк
        """
        return film_score.name
