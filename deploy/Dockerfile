FROM python:latest

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY ./ ./

WORKDIR /app/src

CMD python3 Main.py

