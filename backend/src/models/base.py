from abc import ABC, abstractmethod
from enum import Enum, IntEnum
from typing import Callable, Dict, List, Union
from uuid import UUID, uuid4

import orjson
from pydantic import BaseModel

from core.config import CONFIG


class VotesChoices(IntEnum):
    """Класс с перечислением оценок пользователем."""

    like = 10
    dislike = 0


class SortChoices(str, Enum):
    """Класс с перечислением сортировки."""

    top = 'top'
    new = 'new'
    old = 'old'


def orjson_dumps(data: object, *, default: Callable) -> str:
    """Функция для декодирования в unicode для парсирования объектов на основе pydantic класса.

    Args:
        data: Данные для преобразования
        default: Функция для объектов, которые не могут быть сериализованы.

    Returns:
        str: Строка JSON
    """
    return orjson.dumps(data, default=default).decode()


class OrjsonMixin(BaseModel):
    """Миксин для замены стандартной работы с json на более быструю."""

    class Config:
        """Настройки сериализации."""

        json_loads = orjson.loads
        json_dumps = orjson_dumps


class MongoQuery(ABC, OrjsonMixin):
    """Абстрактная модель запроса, написанный на языке запросов MongoDB."""

    @property
    @abstractmethod
    def params(self) -> Dict:
        """Основной метод модели, представляющий собой параметры запроса в MongoDB."""

    def insert_operations(self, new_doc: Dict) -> Dict:
        """Представление параметров запроса для вставки нового документа.

        Args:
            new_doc: Новый документ

        Returns:
            Dict: Параметры для операции вставки
        """
        return {
            'filter': {'_id': uuid4()},
            'replacement': new_doc,
            'upsert': True,
            'return_document': True,
        }

    def find_operations(self, pipeline: List[Dict]) -> Dict:
        """Представление параметров запроса для поиска и агрегации документов.

        Args:
            pipeline: Список этапов запроса для выборки данных

        Returns:
            Dict: Параметры для операции поиска
        """
        return {
            'pipeline': pipeline,
        }

    def update_operations(self, doc_id: UUID, mapping: Union[Dict, List], upsert: bool = False) -> Dict:
        """Представление параметров запроса для обновления документа.

        Args:
            doc_id: ID документа
            mapping: Изменения документа
            upsert: Выполнение вставки документа, если документа нет

        Returns:
            Dict: Параметры для операции обновления
        """
        return {
            'filter': {'_id': doc_id},
            'update': mapping,
            'upsert': True if CONFIG.fastapi.debug else upsert,
            'return_document': True,
        }

    def delete_operations(self, filtering: Dict) -> Dict:
        """Представление параметров запроса для удаления документа.

        Args:
            filtering: Фильтр, соответствующий удаляемому документу

        Returns:
            Dict: Параметры для операции удаления
        """
        return {
            'filter': filtering,
        }


class APIResponse(ABC, OrjsonMixin):
    """Абстрактная модель ответа API, представляющий данные по HTTP."""
