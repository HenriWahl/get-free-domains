FROM python:3.9

RUN apt -y update
RUN apt -y install python3-pip

COPY . /app
WORKDIR /app
RUN pip3 install -r requirements.txt
RUN chmod +x main.py

RUN useradd -d /app -M app
USER app

ENTRYPOINT ["/app/main.py"]
