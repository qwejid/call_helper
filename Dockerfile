FROM python:3.9
WORKDIR /usr/src/app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

RUN pip install --upgrade pip
COPY ./requirements.txt .

RUN \
 apk add --no-cashe make && \
 apk add --no-cashe postgresql-libs && \
 apk add --no-cashe --virtual .build-deps gss musl-dev postgresql-dev && \
 python3 -m pip install -r requirements.txt --no-cashe-dir && \
 apk --purge del .build-deps

 COPY . .