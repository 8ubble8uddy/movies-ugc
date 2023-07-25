from typing import Optional

from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import CollectionInvalid

from core.config import CONFIG
from core.enums import MongoCollections

mongo: Optional[AsyncIOMotorDatabase] = None


async def create_users_collection():
    """Функция для создания коллекции пользователей."""
    try:
        await mongo.create_collection(
            name=MongoCollections.users.name,
            validator={
                '$jsonSchema': {
                    'bsonType': 'object',
                    'required': ['_id', 'bookmarks'],
                    'properties': {
                        '_id': {'bsonType': 'binData'},
                        'bookmarks': {
                            'bsonType': 'array',
                            'items': {
                                'bsonType': 'object',
                                'required': ['film_id'],
                                'properties': {
                                    'film_id': {'bsonType': 'binData'},
                                },
                            },
                        },
                    },
                },
            },
        )
    except CollectionInvalid:
        pass


async def create_films_collection():
    """Функция для создания коллекции фильмов."""
    try:
        await mongo.create_collection(
            name=MongoCollections.films.name,
            validator={
                '$jsonSchema': {
                    'bsonType': 'object',
                    'required': ['_id', 'rating'],
                    'properties': {
                        '_id': {'bsonType': 'binData'},
                        'rating': {
                            'bsonType': 'object',
                            'required': ['votes'],
                            'properties': {
                                'votes': {
                                    'bsonType': 'array',
                                    'items': {
                                        'bsonType': 'object',
                                        'required': ['user_id', 'score'],
                                        'properties': {
                                            'user_id': {'bsonType': 'binData'},
                                            'score': {'bsonType': 'number'},
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        )
    except CollectionInvalid:
        pass


async def create_reviews_collection():
    """Функция для создания коллекции рецензий."""
    try:
        await mongo.create_collection(
            name=MongoCollections.reviews.name,
            validator={
                '$jsonSchema': {
                    'bsonType': 'object',
                    'required': ['_id', 'rating'],
                    'properties': {
                        '_id': {'bsonType': 'binData'},
                        'author': {'bsonType': 'binData'},
                        'film_id': {'bsonType': 'binData'},
                        'pub_date': {'bsonType': 'date'},
                        'rating': {
                            'bsonType': 'object',
                            'required': ['votes'],
                            'properties': {
                                'votes': {
                                    'bsonType': 'array',
                                    'items': {
                                        'bsonType': 'object',
                                        'required': ['user_id', 'score'],
                                        'properties': {
                                            'user_id': {'bsonType': 'binData'},
                                            'score': {'bsonType': 'number'},
                                        },
                                    },
                                },
                            },
                        },
                    },
                },
            },
        )
    except CollectionInvalid:
        pass
    await mongo[MongoCollections.reviews.name].create_index([('author', 1), ('film_id', 1)], unique=True)


async def start():
    """Функция для подключения к хранилищу данных MongoDB."""
    global mongo
    mongo = AsyncIOMotorDatabase(
        name='ugc_database',
        client=AsyncIOMotorClient(
            host=CONFIG.mongo.host,
            port=CONFIG.mongo.port,
            uuidRepresentation='standard',
        ),
    )
    await create_users_collection()
    await create_films_collection()
    await create_reviews_collection()


async def stop():
    """Функция для отключения от хранилища данных MongoDB."""
    mongo.client.close()


async def get_mongo() -> AsyncIOMotorDatabase:
    """Функция для объявления соединения с MongoDB, которая понадобится при внедрении зависимостей.

    Returns:
        AsyncIOMotorDatabase: Соединение с MongoDB
    """
    return mongo
