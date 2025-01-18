FROM python:3.13.1-slim-bookworm

RUN python -m pip install python-kasa
RUN python -m pip install grpcio-tools
RUN python -m pip install grpcio


RUN mkdir -p /opt/bos/device/drivers/kasa
WORKDIR /opt/bos/device/drivers/kasa

COPY . /opt/bos/device/drivers/kasa/

CMD ["python", "server.py"]