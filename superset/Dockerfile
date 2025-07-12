FROM apache/superset:latest

ARG SUPERSET_SECRET_KEY
ENV SUPERSET_SECRET_KEY=${SUPERSET_SECRET_KEY}

USER root
RUN apt-get update && apt-get install -y g++
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt
USER superset

COPY superset_config.py /app/
# RUN superset db upgrade
# RUN superset init