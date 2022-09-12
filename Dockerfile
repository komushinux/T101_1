#FROM python:3.8-slim-buster
FROM python:3.8-slim-buster

WORKDIR /.

COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .

EXPOSE 5000
CMD python3 generate_and_evaluate.py
