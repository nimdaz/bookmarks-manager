FROM python:3.11-alpine

ENV FLASK_ENV=development
ENV FLASK_APP=app
ENV FLASK_DEBUG=1

WORKDIR /app
ENTRYPOINT ["flask", "run", "--host", "0.0.0.0"]
EXPOSE 5000

COPY ./app/requirements.txt .
RUN pip install -r requirements.txt

COPY ./app .