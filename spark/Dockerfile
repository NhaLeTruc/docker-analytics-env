FROM bitnami/spark:3.5.6-debian-12-r0

USER root

# ----------
# Setup Python and Livy/Spark Deps
#
# Install GCP keys to avoid error:
# "GPG error: https://packages.cloud.google.com/apt cloud-sdk InRelease: The following signatures couldn't be verified because the public key is not available: NO_PUBKEY B53DC80D13EDEF05"
RUN apt-get install apt-transport-https ca-certificates gnupg
RUN echo "deb [signed-by=/usr/share/keyrings/cloud.google.gpg] https://packages.cloud.google.com/apt cloud-sdk main" | tee -a /etc/apt/sources.list.d/google-cloud-sdk.list
RUN curl https://packages.cloud.google.com/apt/doc/apt-key.gpg | apt-key --keyring /usr/share/keyrings/cloud.google.gpg add -
# Livy Requires:
# - mvn (from maven package or maven3 tarball)
# - openjdk-8-jdk (or Oracle JDK 8)
# - Python 2.7+
# - R 3.x
RUN apt update && apt install -yq --no-install-recommends --force-yes \
    curl \
    git \
    python3 python3-setuptools python3-venv python3-pip \
    r-base \
    r-base-core && \
    rm -rf /var/lib/apt/lists/*

ENV PYTHONHASHSEED 0
ENV PYTHONIOENCODING UTF-8
ENV PIP_DISABLE_PIP_VERSION_CHECK 1

# ----------
# Build Livy
# ----------
ARG LIVY_VERSION=0.7.1-incubating
ENV LIVY_HOME /usr/livy
ENV LIVY_CONF_DIR "${LIVY_HOME}/conf"
ENV LIVY_PORT 8998

RUN curl --progress-bar -L --retry 3 \
    "http://archive.apache.org/dist/incubator/livy/${LIVY_VERSION}/apache-livy-${LIVY_VERSION}-bin.zip" \
    -o "./apache-livy-${LIVY_VERSION}-bin.zip" \
  && unzip -qq "./apache-livy-${LIVY_VERSION}-bin.zip" -d /usr \
  && mv "/usr/apache-livy-${LIVY_VERSION}-bin" "${LIVY_HOME}" \
  && rm -rf "./apache-livy-${LIVY_VERSION}-bin.zip" \
  && mkdir "${LIVY_HOME}/logs" \
  && chown -R root:root "${LIVY_HOME}"



HEALTHCHECK CMD curl -f "http://host.docker.internal:${LIVY_PORT}/" || exit 1

CMD ${LIVY_HOME}/bin/livy-server

RUN adduser defaultuser
RUN usermod -u 1000 --gid 0 defaultuser

RUN chown -R defaultuser:defaultuser /opt/bitnami
RUN chmod -R 775 /opt/bitnami

USER defaultuser
WORKDIR /opt/bitnami/

EXPOSE 8998
EXPOSE 8080
EXPOSE 8081
EXPOSE 7077
EXPOSE 18080
