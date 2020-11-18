FROM python:3.8.2-alpine
ADD requirements.txt .
RUN apk update && apk add postgresql-dev gcc python3-dev musl-dev
RUN pip install -r requirements.txt
ADD . /code
EXPOSE 80