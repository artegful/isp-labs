FROM python:3.8.3-alpine as builder

# set project
WORKDIR /usr/src/app
COPY ./requirements.txt .

# set env
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev \
    && pip wheel --no-cache-dir --no-deps --wheel-dir  \
    /usr/src/app/wheels -r requirements.txt


FROM python:3.8.3-alpine

#set env
ENV APP_HOME=/home/app/web

# create app user dir
RUN mkdir -p /home/app \
    && mkdir ${APP_HOME} \
    && mkdir ${APP_HOME}/staticfiles \
    && addgroup -S app  \
    && adduser -S app -G app

#set project
WORKDIR ${APP_HOME}
COPY . ${APP_HOME}

# install dependencies
COPY --from=builder /usr/src/app/wheels /wheels
RUN apk update \
    && apk add libpq \
    && pip install --no-cache /wheels/*

# set user
RUN chown -R app:app ${APP_HOME}
USER app

# run entrypoint.sh
ENTRYPOINT ["/home/app/web/entrypoint.sh"]
