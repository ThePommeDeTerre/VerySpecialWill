from tiangolo/uwsgi-nginx-flask:latest

COPY ./Servidor/requirements.txt /tmp/

RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --requirement /tmp/requirements.txt

COPY . /tmp/