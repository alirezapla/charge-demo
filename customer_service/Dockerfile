FROM python:3.12
WORKDIR /app

COPY ./customer_service /app

RUN python3 -m pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8080
CMD [ "export","PYTHONPATH=." ]