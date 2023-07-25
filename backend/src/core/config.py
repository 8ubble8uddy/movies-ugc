from functools import lru_cache

from pydantic import BaseModel, BaseSettings, Field


class MongoConfig(BaseModel):
    """Класс с настройками подключения к MongoDB.."""

    host: str = 'localhost'
    port: int = 27017
    db: str = 'default'


class LogstashConfig(BaseModel):
    """Класс с настройками подключения к Logstash."""

    host: str = 'localhost'
    port: int = 5044


class SentryConfig(BaseModel):
    """Класс с настройками подключения к Sentry."""

    dsn: str = ''


class FastApiConfig(BaseModel):
    """Класс с настройками подключения к FastAPI."""

    host: str = '0.0.0.0'
    port: int = 8000
    debug: bool = False
    docs: str = 'openapi'
    secret_key: str = 'secret_key'
    title: str = 'API для мониторинга пользовательского контента'


class MainSettings(BaseSettings):
    """Класс с основными настройками проекта."""

    fastapi: FastApiConfig = Field(default_factory=FastApiConfig)
    mongo: MongoConfig = Field(default_factory=MongoConfig)
    sentry: SentryConfig = Field(default_factory=SentryConfig)
    logstash: LogstashConfig = Field(default_factory=LogstashConfig)


@lru_cache()
def get_settings():
    """Функция для создания объекта настроек в едином экземпляре (синглтона).

    Returns:
        MainSettings: Объект с настройками
    """
    return MainSettings(_env_file='.env', _env_nested_delimiter='_')


CONFIG = get_settings()
