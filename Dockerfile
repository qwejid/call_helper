FROM python:3.9

WORKDIR /usr/src/app

# Установить переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Обновить pip
RUN pip install --upgrade pip

# Скопировать файл зависимостей
COPY ./requirements.txt .

# Установить зависимости
RUN apk add --no-cache make postgresql-libs && \
    apk add --no-cache --virtual .build-deps gcc musl-dev postgresql-dev && \
    pip install -r requirements.txt --no-cache-dir && \
    apk del .build-deps

# Скопировать исходный код приложения
COPY . .

