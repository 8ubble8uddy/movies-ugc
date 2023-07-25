from http import HTTPStatus
from uuid import UUID

from fastapi import Body, Depends, Path, Query, Response
from pymongo.errors import DuplicateKeyError

from api.v1.base import Paginator
from services.auth import AuthService
from services.crud import CRUDService, get_crud_service
from core.enums import MongoCollections
from core.exceptions import NotAuthorContentError, UniqueFilmReviewError
from models.base import SortChoices
from models.queries import CreateReview, DestroyReview, ListReview
from models.responses import ReviewResponse


async def create_film_review(
    auth: AuthService = Depends(),
    film_id: UUID = Path(title='ID фильма'),
    text: str = Body(embed=True),
    mongo: CRUDService = Depends(get_crud_service),
) -> ReviewResponse:
    """Представление для создания пользователем рецензии на фильм.

    Args:
        auth: Аутентификация пользователя
        film_id: ID фильма
        text: Текст рецензии
        mongo: Объект для выполнения MongoDB-запросов

    Raises:
        UniqueFilmReviewError: Ошибка 403, если у пользователя уже есть рецензия на данный фильм

    Returns:
        ReviewResponse: Рецензия на фильм
    """
    try:
        review = await mongo.create(
            collection=MongoCollections.reviews,
            query=CreateReview(author=auth.user_id, film_id=film_id, text=text),
        )
    except DuplicateKeyError:
        raise UniqueFilmReviewError(status_code=HTTPStatus.FORBIDDEN)
    return review


async def delete_film_review(
    auth: AuthService = Depends(),
    film_id: UUID = Path(title='Фильм ID'),
    review_id: UUID = Path(title='Ревью ID'),
    mongo: CRUDService = Depends(get_crud_service),
) -> Response:
    """Представление для удаления пользователем рецензии на фильм.

    Args:
        auth: Аутентификация пользователя
        film_id: ID фильма
        review_id: ID рецензии
        mongo: Объект для выполнения MongoDB-запросов

    Raises:
        NotAuthorContentError: Ошибка 403, если пользователь не является автором рецензии

    Returns:
        Response: HTTP-ответ с кодом 204
    """
    review = await mongo.delete(
        collection=MongoCollections.reviews,
        query=DestroyReview(id=review_id, author=auth.user_id),
    )
    if not review:
        raise NotAuthorContentError(status_code=HTTPStatus.FORBIDDEN)
    return Response(status_code=HTTPStatus.NO_CONTENT)


async def get_film_reviews(
    film_id: UUID = Path(title='Фильм ID'),
    sort: SortChoices = Query(default=SortChoices.top),
    page: Paginator = Depends(),
    mongo: CRUDService = Depends(get_crud_service),
) -> ReviewResponse:
    """Представление для получения списка рецензий на фильм.

    Args:
        film_id: ID фильма
        sort: Параметр сортировки
        page: Параметры страницы
        mongo: Объект для выполнения MongoDB-запросов

    Returns:
        ReviewResponse: Список рецензий на фильм
    """
    reviews = await mongo.search(
        collection=MongoCollections.reviews,
        query=ListReview(film_id=film_id, sort=sort, offset=page.offset, limit=page.limit),
    )
    return reviews
