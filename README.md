## Movies UGC

[![python](https://img.shields.io/static/v1?label=python&message=3.8%20|%203.9%20|%203.10&color=informational)](https://github.com/8ubble8uddy/movies-ugc/actions/workflows/main.yml)
[![dockerfile](https://img.shields.io/static/v1?label=dockerfile&message=published&color=2CB3E8)](https://hub.docker.com/r/8ubble8uddy/ugc_api)
[![last updated](https://img.shields.io/static/v1?label=last%20updated&message=february%202023&color=yellow)](https://img.shields.io/static/v1?label=last%20updated&message=february%202022&color=yellow)
[![lint](https://img.shields.io/static/v1?label=lint&message=flake8%20|%20mypy&color=brightgreen)](https://github.com/8ubble8uddy/movies-ugc/actions/workflows/main.yml)
[![code style](https://img.shields.io/static/v1?label=code%20style&message=WPS&color=orange)](https://wemake-python-styleguide.readthedocs.io/en/latest/)
[![platform](https://img.shields.io/static/v1?label=platform&message=linux%20|%20macos&color=inactive)](https://github.com/8ubble8uddy/movies-ugc/actions/workflows/main.yml)

### **Описание**

_Целью данного проекта является реализация сервиса для удобного хранения аналитической информации и UGC. К UGC относится всё, чем пользователь дополняет ваш сайт: например, лайки, закладки и рецензии фильмов. В связи с этим хранилище должно не только хранить большие данные, но и предоставлять быстрый доступ к ним (за менее 200 миллисекунд). Поэтому в рамках проекта было проведено исследование на соответствие вышеперечисленным требованиям, по итогам которого выбор остановился на документоориентированной NoSQL базе данных [MongoDB](https://www.mongodb.com). Для прослойки кода в виде API используется асинхронный фреймворк [FastAPI](https://fastapi.tiangolo.com). Проект запускается через прокси-сервер [NGINX](https://nginx.org), который является точкой входа для веб-приложения._

### **Технологии**

```Python``` ```FastAPI``` ```MongoDB``` ```NGINX``` ```Gunicorn``` ```Docker```

### **Как запустить проект:**

Клонировать репозиторий и перейти внутри него в директорию ```/infra```:
```
git clone https://github.com/8ubble8uddy/movies-ugc.git
```
```
cd movies-ugc/infra/
```

Создать файл .env и добавить настройки для проекта:
```
nano .env
```
```
# MongoDB
MONGO_HOST=mongo
MONGO_PORT=27017
```

Развернуть и запустить проект в контейнерах:
```
docker-compose up
```

Документация API будет доступна по адресу:
```
http://127.0.0.1/openapi
```

### Автор: Герман Сизов