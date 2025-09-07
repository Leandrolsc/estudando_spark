FROM bitnami/spark:4.0.0

USER root

RUN apt-get update && apt-get install -y python3-pip
COPY requirements.txt /
RUN pip3 install --no-cache-dir -r /requirements.txt

RUN chown -R 1001:0 /opt/bitnami/spark/data \
    && mkdir -p /opt/bitnami/spark/spark-warehouse \
    && chown -R 1001:0 /opt/bitnami/spark/spark-warehouse

ENV HOME=/opt/bitnami/spark

USER 1001

