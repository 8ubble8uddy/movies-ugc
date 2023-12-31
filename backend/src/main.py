import logging

import sentry_sdk
import uvicorn
from fastapi import APIRouter, Depends, FastAPI, Header
from fastapi.responses import ORJSONResponse
from sentry_sdk.integrations.fastapi import FastApiIntegration

from api.urls import routes
from core.config import CONFIG
from core.exceptions import exception_handlers
from core.logger import LOGGING, RequestIdFilter
from db import mongo

if sentry := CONFIG.sentry.dsn:
    sentry_sdk.init(sentry, integrations=[FastApiIntegration()])


async def logging_request_id(request_id: str = Header(default=None, alias='X-Request-Id')):
    """Функция для добавления в лог информацию о `request-id`, с которым был выполнен запрос.

    Args:
        request_id: X-Request-Id, переданный через заголовок запроса
    """
    logger = logging.getLogger('uvicorn.access')
    logger.addFilter(RequestIdFilter(request_id))


app = FastAPI(
    title=CONFIG.fastapi.title,
    description='Сервис для хранения аналитической информации и UGC',
    version='1.0.0',
    docs_url=f'/{CONFIG.fastapi.docs}',
    openapi_url=f'/{CONFIG.fastapi.docs}.json',
    default_response_class=ORJSONResponse,
    dependencies=[Depends(logging_request_id)],
    exception_handlers=exception_handlers,
)


@app.on_event('startup')
async def startup():
    """Подключаемся к хранилищу данных MongoDB при старте сервера."""
    await mongo.start()


@app.on_event('shutdown')
async def shutdown():
    """Отключаемся от хранилищу данных MongoDB при выключении сервера."""
    await mongo.stop()


app.include_router(APIRouter(routes=routes), prefix='/api/v1')


if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=CONFIG.fastapi.host,
        port=CONFIG.fastapi.port,
        log_config=LOGGING,
        log_level=logging.DEBUG,
    )
