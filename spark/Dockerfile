FROM bitnami/spark:3.5.6-debian-12-r0

USER root

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

RUN adduser defaultuser
RUN usermod -u 1000 --gid 0 defaultuser

USER defaultuser

WORKDIR /notebooks

EXPOSE 8888
EXPOSE 8080
EXPOSE 8081
EXPOSE 7077
EXPOSE 18080
