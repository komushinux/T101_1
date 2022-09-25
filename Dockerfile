FROM python:3.8-slim-buster

RUN mkdir app

COPY ./ ./app

WORKDIR /app

CMD ["python3", "generate_and_evaluate.py"]