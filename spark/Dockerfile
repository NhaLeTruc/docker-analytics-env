FROM bitnami/spark:3.5.6-debian-12-r0

USER root

COPY requirements.txt requirements.txt
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

RUN echo 'PYSPARK_PYTHON=/opt/bitnami/python' >> ~/.bashrc
RUN echo 'SPARK_MASTER_HOST=0.0.0.0' >> ~/.bashrc
RUN . ~/.bashrc

RUN adduser defaultuser \
    usermod -u 1000 --gid 0 defaultuser

USER defaultuser

RUN mkdir -p /opt/bitnami/workspace
WORKDIR /opt/bitnami/workspace

EXPOSE 8888
EXPOSE 8080
EXPOSE 8081
EXPOSE 7077
EXPOSE 18080
