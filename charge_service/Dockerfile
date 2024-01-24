FROM python:3.12

ENV PYTHONDONTWRITEBYTECODE 1,PYTHONUNBUFFERED 1
COPY ./charge_service /app
WORKDIR /app

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD [ "export","PYTHONPATH=." ]