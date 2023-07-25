from enum import Enum


class MongoCollections(Enum):
    """Класс с перечислением коллекций в MongoDB."""

    users = 'users'
    films = 'films'
    reviews = 'reviews'
