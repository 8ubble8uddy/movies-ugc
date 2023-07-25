import logging
from functools import lru_cache
from http import HTTPStatus
from typing import Dict, List
from uuid import UUID

from fastapi import Depends, HTTPException
from motor.motor_asyncio import AsyncIOMotorDatabase
from pymongo.errors import ServerSelectionTimeoutError

from core.enums import MongoCollections
from db.mongo import get_mongo
from models.base import MongoQuery


class CRUDService:
    """Класс сервиса для выполнения основных операций по обработке данных в MongoDB."""

    def __init__(self, mongo: AsyncIOMotorDatabase):
        """При инициализации класса принимает клиент базы данных MongoDB.

        Args:
            mongo: Клиент MongoDB
        """
        self.mongo = mongo

    async def create(self, collection: MongoCollections, query: MongoQuery) -> Dict:
        """Cоздание документа в коллекции.

        Args:
            collection: Коллекция с документами
            query: Запрос на языке запросов MongoDB

        Raises:
            HTTPException: Ошибка, если сервер MongoDB недоступен для операции

        Returns:
            Dict: Новый документ
        """
        try:
            result = await self.mongo[collection.name].find_one_and_replace(**query.params)
        except ServerSelectionTimeoutError as exc:
            logging.error(exc)
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        return result or {}

    async def retrieve(self, collection: MongoCollections, doc_id: UUID) -> Dict:
        """Чтение документа по ID в коллекции.

        Args:
            collection: Коллекция с документами
            doc_id: ID документа

        Raises:
            HTTPException: Ошибка, если сервер MongoDB недоступен для операции

        Returns:
            Dict: Документ по ID
        """
        try:
            result = await self.mongo[collection.name].find_one(doc_id)
        except ServerSelectionTimeoutError as exc:
            logging.error(exc)
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        return result or {}

    async def search(self, collection: MongoCollections, query: MongoQuery) -> List[Dict]:
        """Поиск документов в коллекции.

        Args:
            collection: Коллекция с документами
            query: Запрос на языке запросов MongoDB

        Raises:
            HTTPException: Ошибка, если сервер MongoDB недоступен для операции

        Returns:
            List: Список документов
        """
        try:
            result = await self.mongo[collection.name].aggregate(**query.params).to_list(None)
        except ServerSelectionTimeoutError as exc:
            logging.error(exc)
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        return result

    async def update(self, collection: MongoCollections, query: MongoQuery) -> Dict:
        """Обновление документа в коллекции.

        Args:
            collection: Коллекция с документами
            query: Запрос на языке запросов MongoDB

        Raises:
            HTTPException: Ошибка, если сервер MongoDB недоступен для операции

        Returns:
            Dict: Документ после обновления
        """
        try:
            result = await self.mongo[collection.name].find_one_and_update(**query.params)
        except ServerSelectionTimeoutError as exc:
            logging.error(exc)
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        return result or {}

    async def delete(self, collection: MongoCollections, query: MongoQuery) -> Dict:
        """Удаление документа из коллекции.

        Args:
            collection: Коллекция с документами
            query: Запрос на языке запросов MongoDB

        Raises:
            HTTPException: Ошибка, если сервер MongoDB недоступен для операции

        Returns:
            Dict: Документ для удаления
        """
        try:
            result = await self.mongo[collection.name].find_one_and_delete(**query.params)
        except ServerSelectionTimeoutError as exc:
            logging.error(exc)
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST)
        return result


@lru_cache()
def get_crud_service(mongo: AsyncIOMotorDatabase = Depends(get_mongo)) -> CRUDService:
    """Функция для создания объекта сервиса CRUDService в едином экземпляре (синглтона).

    Args:
        mongo: Соединение с MongoDB

    Returns:
        CRUDService: Сервис для обработки данных в MongoDB
    """
    return CRUDService(mongo)
