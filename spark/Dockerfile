FROM bitnami/spark:3.5.6-debian-12-r0

USER root

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt
RUN jupyter server extension enable --py sparkmagic

RUN cd $(pip show sparkmagic)
RUN jupyter-kernelspec install sparkmagic/kernels/sparkkernel \
    jupyter-kernelspec install sparkmagic/kernels/pysparkkernel \
    jupyter-kernelspec install sparkmagic/kernels/sparkrkernel

RUN adduser defaultuser
RUN usermod -u 1000 --gid 0 defaultuser

RUN chown -R defaultuser:defaultuser /opt/bitnami
RUN chmod -R 775 /opt/bitnami

USER defaultuser
WORKDIR /opt/bitnami/notebooks

EXPOSE 8888
EXPOSE 8080
EXPOSE 8081
EXPOSE 7077
EXPOSE 18080
