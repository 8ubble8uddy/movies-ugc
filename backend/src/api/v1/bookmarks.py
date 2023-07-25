from uuid import UUID

from fastapi import Depends, Path

from api.v1.base import Paginator
from services.auth import AuthService
from services.crud import CRUDService, get_crud_service
from core.enums import MongoCollections
from models.queries import AddBookmark, RemoveBookmark
from models.responses import BookmarkResponse


async def bookmark_film(
    auth: AuthService = Depends(),
    film_id: UUID = Path(title='ID фильма'),
    mongo: CRUDService = Depends(get_crud_service),
) -> BookmarkResponse:
    """Представление для добавления фильма в закладки пользователя.

    Args:
        auth: Аутентификация пользователя
        film_id: ID фильма
        mongo: Объект для выполнения MongoDB-запросов

    Returns:
        BookmarkResponse: Список фильмов, отложенных пользователем на потом
    """
    user = await mongo.update(
        collection=MongoCollections.users,
        query=AddBookmark(user_id=auth.user_id, film_id=film_id),
    )
    return user.get('bookmarks', [])


async def unbookmark_film(
    auth: AuthService = Depends(),
    film_id: UUID = Path(title='Фильм ID'),
    mongo: CRUDService = Depends(get_crud_service),
) -> BookmarkResponse:
    """Представление для изъятия фильма из закладок пользователя.

    Args:
        auth: Аутентификация пользователя
        film_id: ID фильма
        mongo: Объект для выполнения MongoDB-запросов

    Returns:
        BookmarkResponse: Список фильмов, отложенных пользователем на потом
    """
    user = await mongo.update(
        collection=MongoCollections.users,
        query=RemoveBookmark(user_id=auth.user_id, film_id=film_id),
    )
    return user.get('bookmarks', [])


async def get_user_bookmarks(
    auth: AuthService = Depends(),
    page: Paginator = Depends(),
    mongo: CRUDService = Depends(get_crud_service),
) -> BookmarkResponse:
    """Представление для получения закладок пользователя.

    Args:
        auth: Аутентификация пользователя
        page: Параметры страницы
        mongo: Объект для выполнения MongoDB-запросов

    Returns:
        BookmarkResponse: Список фильмов, отложенных пользователем на потом
    """
    user = await mongo.retrieve(collection=MongoCollections.users, doc_id=auth.user_id)
    return user.get('bookmarks', [])[page.slice]
