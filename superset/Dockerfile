FROM apache/superset:latest

ARG SUPERSET_SECRET_KEY
ENV SUPERSET_SECRET_KEY=${SUPERSET_SECRET_KEY}

USER root

RUN apt-get update && apt-get install -y g++
COPY requirements.txt /app/requirements.txt
RUN pip install -r /app/requirements.txt

ENV ADMIN_USERNAME $ADMIN_USERNAME
ENV ADMIN_EMAIL $ADMIN_EMAIL
ENV ADMIN_PASSWORD $ADMIN_PASSWORD

COPY ./superset-init.sh /superset-init.sh

COPY superset_config.py /app/
ENV SUPERSET_CONFIG_PATH /app/superset_config.py

USER superset
ENTRYPOINT [ "/superset-init.sh" ]