FROM bitnami/spark:3.5.6-debian-12-r0

USER root

ARG LIVY_VERSION=0.7.1-incubating
ENV LIVY_HOME /opt/bitnami/livy
ENV LIVY_CONF_DIR "${LIVY_HOME}/conf"
ENV LIVY_PORT 8998
WORKDIR /opt/bitnami/

RUN apt update && apt install unzip

RUN curl --progress-bar -L --retry 3 "http://archive.apache.org/dist/incubator/livy/${LIVY_VERSION}/apache-livy-${LIVY_VERSION}-bin.zip" -O \
  && unzip -qq "apache-livy-${LIVY_VERSION}-bin.zip" \
  && mv "apache-livy-${LIVY_VERSION}-bin" "${LIVY_HOME}" \
  && rm -rf "apache-livy-${LIVY_VERSION}-bin.zip" \
  && mkdir ${LIVY_HOME}/logs

RUN adduser defaultuser
RUN usermod -u 1000 --gid 0 defaultuser

RUN chown -R defaultuser:defaultuser /opt/bitnami
RUN chmod -R 775 /opt/bitnami

USER defaultuser

EXPOSE 8998
EXPOSE 8080
EXPOSE 8081
EXPOSE 7077
EXPOSE 18080
