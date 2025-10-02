FROM spark:4.0.0-java21-python3

USER root

COPY requirements.txt /opt/spark/work-dir/
RUN pip install --no-cache-dir -r /opt/spark/work-dir/requirements.txt

RUN chown -R spark:spark /opt/spark/work-dir

#USER spark #Comentado para rodar como root
 
WORKDIR /opt/spark/work-dir

