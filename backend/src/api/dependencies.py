from http import HTTPStatus
from uuid import UUID

from fastapi import Depends

from services.crud import CRUDService, get_crud_service
from core.config import CONFIG
from core.enums import MongoCollections
from core.exceptions import NotFoundFilmError, NotFoundReviewError


async def check_film_exists(film_id: UUID, mongo: CRUDService = Depends(get_crud_service)):
    """Функция для проверки наличия фильма, с целью внедрения зависимости.

    Args:
        film_id: ID фильма
        mongo: Объект для выполнения MongoDB-запросов

    Raises:
        NotFoundFilmError: Ошибка 404, если фильм не найден
    """
    if not CONFIG.fastapi.debug:
        if not (await mongo.retrieve(MongoCollections.films, film_id)):
            raise NotFoundFilmError(status_code=HTTPStatus.NOT_FOUND)


async def check_review_exists(review_id: UUID, mongo: CRUDService = Depends(get_crud_service)):
    """Функция для проверки наличия рецензии, с целью внедрения зависимости.

    Args:
        review_id: ID рецензии
        mongo: Объект для выполнения MongoDB-запросов

    Raises:
        NotFoundReviewError: Ошибка 404, если рецензии не найдена
    """
    if not (await mongo.retrieve(MongoCollections.reviews, review_id)):
        raise NotFoundReviewError(status_code=HTTPStatus.NOT_FOUND)
