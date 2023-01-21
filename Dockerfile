FROM python:3.8-slim-buster

ENV BASE_DIR=/summarizer
WORKDIR ${BASE_DIR}

COPY requirements.txt ${BASE_DIR}/

RUN pip install -r requirements.txt
