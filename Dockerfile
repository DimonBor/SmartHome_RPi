FROM python:3.8-buster as builder

WORKDIR /app

RUN apt-get update
RUN apt-get install -y --no-install-recommends build-essential gcc

COPY requirements.txt requirements.txt

RUN pip3 install --user -r requirements.txt

FROM python:3.8-slim-buster AS build-image

COPY --from=builder /root/.local /root/.local
COPY . .

CMD [ "python3", "main.py"]
