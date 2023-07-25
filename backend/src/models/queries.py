from datetime import datetime
from typing import Dict
from uuid import UUID

from pydantic import Field, validator

from models.base import MongoQuery, SortChoices, VotesChoices


class AddBookmark(MongoQuery):
    """Модель запроса для добавления фильма в закладки пользователя."""

    user_id: UUID
    film_id: UUID

    @property
    def params(self) -> Dict:
        """Параметры запроса для обновления списка закладок пользователя.

        Returns:
            Dict: Запрос для обновления документа с пользователем
        """
        mapping = {}
        mapping['$addToSet'] = {'bookmarks': {'film_id': self.film_id}}
        return self.update_operations(self.user_id, mapping, upsert=True)


class RemoveBookmark(MongoQuery):
    """Модель запроса для изъятия фильма из закладок пользователя."""

    user_id: UUID
    film_id: UUID

    @property
    def params(self) -> Dict:
        """Параметры запроса для обновления списка закладок пользователя.

        Returns:
            Dict: Запрос для обновления документа с пользователем
        """
        mapping = {}
        mapping['$pull'] = {'bookmarks': {'film_id': self.film_id}}
        return self.update_operations(self.user_id, mapping)


class AddRating(MongoQuery):
    """Модель запроса для установления пользовательской оценки."""

    user_id: UUID
    source_id: UUID
    score: VotesChoices

    @property
    def params(self) -> Dict:
        """Параметры запроса для обновления рейтинга фильма или рецензии.

        Returns:
            Dict: Запрос для обновления документа с фильмом или рецензией
        """
        pipeline = []
        pipeline.append(
            {'$set': {'rating.votes': {
                '$concatArrays': [
                    [{'user_id': self.user_id, 'score': self.score.value}],
                    {'$filter': {
                        'input': {'$ifNull': ['$rating.votes', []]},
                        'cond': {'$ne': ['$$this.user_id', self.user_id]},
                    }},
                ]},
            }},
        )
        return self.update_operations(self.source_id, pipeline)


class RemoveRating(MongoQuery):
    """Модель запроса для снятия пользовательской оценки."""

    user_id: UUID
    source_id: UUID

    @property
    def params(self) -> Dict:
        """Параметры запроса для обновления рейтинга фильма или рецензии.

        Returns:
            Dict: Запрос для обновления документа с фильмом или рецензией
        """
        mapping = {}
        mapping['$pull'] = {'rating.votes': {'user_id': {'$eq': self.user_id}}}
        return self.update_operations(self.source_id, mapping)


class CreateReview(MongoQuery):
    """Модель запроса для создания пользователем рецензии на фильм."""

    author: UUID
    film_id: UUID
    text: str
    pub_date: datetime = Field(default_factory=datetime.now)

    @property
    def params(self) -> Dict:
        """Параметры запроса для вставки рецензии фильма.

        Returns:
            Dict: Запрос для вставки документа с рецензией
        """
        new_doc = self.dict()
        new_doc['rating'] = {'votes': []}
        return self.insert_operations(new_doc)


class DestroyReview(MongoQuery):
    """Модель запроса для удаления пользователем рецензии на фильм."""

    id: UUID = Field(alias='_id')
    author: UUID

    @property
    def params(self) -> Dict:
        """Параметры запроса для удаления рецензии фильма.

        Returns:
            Dict: Запрос для удаления документа с рецензией
        """
        filtering = self.dict(by_alias=True)
        return self.delete_operations(filtering)

    class Config:
        """Настройки валидации."""

        allow_population_by_field_name = True


class ListReview(MongoQuery):
    """Модель запроса для получения списка рецензий по фильму с возможностью гибкой сортировки."""

    film_id: UUID
    sort: SortChoices
    offset: int
    limit: int

    @validator('sort')
    def ordering(cls, sort: SortChoices) -> Dict:
        """Валидация параметра сортировки для приведения его в данные для запроса.

        Args:
            sort: Параметр сортировки

        Returns:
            Dict: Данные для запроса с сортировкой
        """
        result = {}
        if sort == SortChoices.top:
            result.update({'average_rating': -1})
        elif sort == SortChoices.new:
            result.update({'pub_date': -1})
        elif sort == SortChoices.old:
            result.update({'pub_date': 1})
        return result

    @property
    def params(self) -> Dict:
        """Параметры запроса для получения рецензий по фильму.

        Returns:
            Dict: Запрос для поиска документов с рецензиями
        """
        pipeline = []
        pipeline.extend([
            {'$match': {'film_id': self.film_id}},
            {'$lookup': {
                'from': 'films',
                'let': {'author': '$author'},
                'pipeline': [
                    {'$match': {'_id': self.film_id}},
                    {'$unwind': '$rating.votes'},
                    {'$match': {'$expr': {'$eq': ['$rating.votes.user_id', '$$author']}}},
                ],
                'as': 'films',
            }},
            {'$addFields': {
                'film_score': {
                    '$first': '$films.rating.votes.score',
                },
                'likes': {'$size': {'$filter': {
                    'input': '$rating.votes',
                    'cond': {'$eq': ['$$this.score', VotesChoices.like.value]},
                }}},
                'dislikes': {'$size': {'$filter': {
                    'input': '$rating.votes',
                    'cond': {'$eq': ['$$this.score', VotesChoices.dislike.value]},
                }}},
                'average_rating': {
                    '$avg': '$rating.votes.score',
                },
            }},
            {'$sort': self.sort},
            {'$skip': self.offset},
            {'$limit': self.limit},
        ])
        return self.find_operations(pipeline)
