import logging
from http import HTTPStatus
from typing import Dict
from uuid import UUID, uuid4

import jwt
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt.exceptions import ExpiredSignatureError

from core.config import CONFIG

security = HTTPBearer(auto_error=not CONFIG.fastapi.debug)


class AuthService:
    """Класс сервиса для аутентификации пользователя."""

    def __init__(self, credentials: HTTPAuthorizationCredentials = Depends(security)):
        """При инициализации класса принимает в HTTP-запросе заголовок с JWT-токеном.

        Args:
            credentials: Заголовок авторизации HTTP с токеном
        """
        if credentials:
            self.token = credentials.credentials
        else:
            self.token = jwt.encode({'user_id': str(uuid4())}, key=CONFIG.fastapi.secret_key, algorithm='HS256')

    @property
    def user_id(self) -> UUID:
        """Свойство с ID пользователя из заявок (claims) токена.

        Raises:
            HTTPException: Ошибка идентификации

        Returns:
            UUID: Уникальный идентификатор пользователя
        """
        claims = self.decode_token()
        if not (user_id := claims.get('user_id')):
            logging.critical('Проблема с идентификацией пользователей: В токене нет ID пользователя!')
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        return user_id

    def decode_token(self) -> Dict:
        """Декодирование JWT-токена.

        Raises:
            HTTPException: Ошибка авторизации

        Returns:
            Dict: Содержимое токена
        """
        try:
            payload = jwt.decode(self.token, key=CONFIG.fastapi.secret_key, algorithms=['HS256'])
        except ExpiredSignatureError:
            raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED)
        except Exception as exc:
            logging.error('Проблема с авторизацией пользователей: {exc}!'.format(exc=exc))
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        return payload
