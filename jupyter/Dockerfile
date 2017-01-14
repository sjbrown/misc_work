FROM jupyter/datascience-notebook

USER root

RUN apt-get update && apt-get install -y \
    postgresql \
    libpq-dev

RUN pip install sqlalchemy
RUN pip install psycopg2
RUN pip install arrow
RUN pip2 install sqlalchemy
RUN pip2 install psycopg2
RUN pip2 install arrow

RUN apt-get clean

ADD notebook.py /opt/conda/lib/python3.5/
ADD notebook.py /opt/conda/envs/python2/lib/python2.7/
ADD notebook.py /opt/conda/pkgs/python-2.7.12-1/lib/python2.7/
ADD notebook.py /opt/conda/pkgs/python-3.5.2-0/lib/python3.5/
ADD notebook.py /usr/lib/python2.7/
ADD *ipynb /home/jovyan/work/

RUN mkdir /home/jovyan/work/user
RUN chmod a+rw /home/jovyan/work/*
