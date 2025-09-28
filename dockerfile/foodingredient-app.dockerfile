FROM python:3.13.7-slim as base

FROM base as builder
COPY requirements.txt /requirements.txt

RUN apt-get update -qqy && \
    apt-get -qqy install gcc
RUN pip install --user -r /requirements.txt

FROM base

ENV APP_NAME=app
ENV PORT=5566
ENV IMAGE_FOLDER=/var/html/image
ENV CONFIG=/opt/config/.env

WORKDIR /app
COPY --from=builder /root/.local /root/.local
COPY ./food /app/food
COPY ./logging.yml /app/logging.yml

EXPOSE ${PORT}

ENTRYPOINT [ "/bin/bash", "-c", "python app.py" ]