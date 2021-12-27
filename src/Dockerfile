FROM python:3.8

RUN apt update -y && \
    apt install vim -y 

WORKDIR "/app"

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . /app

CMD [ "python", "app.py" ]

EXPOSE 5000


