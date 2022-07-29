FROM python:3.10.4

WORKDIR /data_loader

COPY ./requirements.txt /data_loader/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /data_loader/requirements.txt

COPY . .

CMD [ "python", "data_loader.py" ]
