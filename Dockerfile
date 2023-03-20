FROM python:3.8

WORKDIR /app

RUN apt-get update && \
    apt-get install -y curl wget openjdk-11-jdk

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . .

# EXPOSE 80

#RUN python main.py

WORKDIR /app

CMD [ "./app/entrypoint.sh" ]

# CMD ["flask", "run", "--host=0.0.0.0", "--port=80"]