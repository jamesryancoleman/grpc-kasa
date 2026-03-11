FROM jamescoleman/bospy

RUN python -m pip install python-kasa

RUN mkdir -p /opt/bos/device/drivers/kasa
WORKDIR /opt/bos/device/drivers/kasa

COPY . /opt/bos/device/drivers/kasa/

CMD ["python", "server.py"]