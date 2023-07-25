from typing import Optional

from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse


class UGCException(HTTPException):
    """Пользовательское HTTP-исключение."""

    message: Optional[str] = None

    def __init__(self, status_code: int):
        """При инициализации исключения ожидает код ошибки HTTP.

        Args:
            status_code: Код ошибки
        """
        super().__init__(status_code, detail=self.message)

    @staticmethod
    def handler(request: Request, exc: HTTPException) -> JSONResponse:
        """Функция для выдачи HTTP-ответа при возникновении пользовательского исключения.

        Args:
            request: Запрос клиента
            exc: HTTP-исключение

        Returns:
            JSONResponse: Ответ сервера
        """
        return JSONResponse(content={'message': exc.detail}, status_code=exc.status_code)


class NotFoundFilmError(UGCException):
    """Ошибка из-за отсутствия фильма в базе данных."""

    message: str = 'Фильм не найден!'


class NotFoundReviewError(UGCException):
    """Ошибка из-за отсутствия рецензии в базе данных."""

    message: str = 'Рецензия не найдена!'


class UniqueFilmReviewError(UGCException):
    """Ошибка из-за нарушения ограничения уникальности автора рецензии и рецензируемого фильма."""

    message: str = 'Создание больше одной рецензии на фильм запрещено!'


class NotAuthorContentError(UGCException):
    """Ошибка из-за нарушения ограничения использования пользовательского контента."""

    message: str = 'Изменение чужого контента запрещено!'


exception_handlers = {exc: exc.handler for exc in UGCException.__subclasses__()}
