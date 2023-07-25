from http import HTTPStatus
from uuid import UUID

from fastapi import Body, Depends, Path

from services.auth import AuthService
from services.crud import CRUDService, get_crud_service
from core.enums import MongoCollections
from core.exceptions import NotFoundFilmError, NotFoundReviewError
from models.base import VotesChoices
from models.queries import AddRating, RemoveRating
from models.responses import RatingResponse


async def rate_film(
    auth: AuthService = Depends(),
    film_id: UUID = Path(title='Фильм ID'),
    score: VotesChoices = Body(embed=True),
    mongo: CRUDService = Depends(get_crud_service),
) -> RatingResponse:
    """Представление для установления пользовательской оценки фильму.

    Args:
        auth: Аутентификация пользователя
        film_id: ID фильма
        score: Оценка пользователя
        mongo: Объект для выполнения MongoDB-запросов

    Raises:
        NotFoundFilmError: Ошибка 404, если фильм не найден

    Returns:
        RatingResponse: Рейтинг фильма
    """
    film = await mongo.update(
        collection=MongoCollections.films,
        query=AddRating(user_id=auth.user_id, source_id=film_id, score=score),
    )
    if not film:
        raise NotFoundFilmError(status_code=HTTPStatus.NOT_FOUND)
    return film.get('rating', {})


async def unrate_film(
    auth: AuthService = Depends(),
    film_id: UUID = Path(title='Фильм ID'),
    mongo: CRUDService = Depends(get_crud_service),
) -> RatingResponse:
    """Представление для снятия пользовательской оценки фильму.

    Args:
        auth: Аутентификация пользователя
        film_id: ID фильма
        mongo: Объект для выполнения MongoDB-запросов

    Raises:
        NotFoundFilmError: Ошибка 404, если фильм не найден

    Returns:
        RatingResponse: Рейтинг фильма
    """
    film = await mongo.update(
        collection=MongoCollections.films,
        query=RemoveRating(user_id=auth.user_id, source_id=film_id),
    )
    if not film:
        raise NotFoundFilmError(status_code=HTTPStatus.NOT_FOUND)
    return film.get('rating', {})


async def get_film_rating(
    film_id: UUID = Path(title='Фильм ID'),
    mongo: CRUDService = Depends(get_crud_service),
) -> RatingResponse:
    """Представление для получения рейтинга фильма.

    Args:
        film_id: ID фильма
        mongo: Объект для выполнения MongoDB-запросов

    Raises:
        NotFoundFilmError: Ошибка 404, если фильм не найден

    Returns:
        RatingResponse: Рейтинг фильма
    """
    film = await mongo.retrieve(collection=MongoCollections.films, doc_id=film_id)
    if not film:
        raise NotFoundFilmError(status_code=HTTPStatus.NOT_FOUND)
    return film.get('rating', {})


async def rate_review(
    auth: AuthService = Depends(),
    film_id: UUID = Path(title='Фильм ID'),
    review_id: UUID = Path(title='Ревью ID'),
    score: VotesChoices = Body(embed=True),
    mongo: CRUDService = Depends(get_crud_service),
) -> RatingResponse:
    """Представление для установления пользовательской оценки рецензии на фильм.

    Args:
        auth: Аутентификация пользователя
        film_id: ID фильма
        review_id: ID рецензии
        score: Оценка пользователя
        mongo: Объект для выполнения MongoDB-запросов

    Raises:
        NotFoundReviewError: Ошибка 404, если рецензия не найдена

    Returns:
        RatingResponse: Рейтинг рецензии на фильм
    """
    review = await mongo.update(
        collection=MongoCollections.reviews,
        query=AddRating(user_id=auth.user_id, source_id=review_id, score=score),
    )
    if not review:
        raise NotFoundReviewError(status_code=HTTPStatus.NOT_FOUND)
    return review.get('rating', {})


async def unrate_review(
    auth: AuthService = Depends(),
    film_id: UUID = Path(title='Фильм ID'),
    review_id: UUID = Path(title='Ревью ID'),
    mongo: CRUDService = Depends(get_crud_service),
) -> RatingResponse:
    """Представление для снятия пользовательской оценки рецензии на фильм.

    Args:
        auth: Аутентификация пользователя
        film_id: ID фильма
        review_id: ID рецензии
        mongo: Объект для выполнения MongoDB-запросов

    Raises:
        NotFoundReviewError: Ошибка 404, если рецензия не найдена

    Returns:
        RatingResponse: Рейтинг рецензии на фильм
    """
    review = await mongo.update(
        collection=MongoCollections.reviews,
        query=RemoveRating(user_id=auth.user_id, source_id=review_id),
    )
    if not review:
        raise NotFoundReviewError(status_code=HTTPStatus.NOT_FOUND)
    return review.get('rating', {})


async def get_review_rating(
    film_id: UUID = Path(title='Фильм ID'),
    review_id: UUID = Path(title='Ревью ID'),
    mongo: CRUDService = Depends(get_crud_service),
) -> RatingResponse:
    """Представление для получения рейтинга рецензии на фильм.

    Args:
        film_id: ID фильма
        review_id: ID рецензии
        mongo: Объект для выполнения MongoDB-запросов

    Raises:
        NotFoundReviewError: Ошибка 404, если рецензия не найдена

    Returns:
        RatingResponse: Рейтинг рецензии на фильм
    """
    review = await mongo.retrieve(collection=MongoCollections.reviews, doc_id=review_id)
    if not review:
        raise NotFoundReviewError(status_code=HTTPStatus.NOT_FOUND)
    return review.get('rating', {})
