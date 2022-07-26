FROM python:3.10.4

WORKDIR /backend

COPY ./requirements.txt /backend/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /backend/requirements.txt

COPY . .

CMD [ "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000" ]
