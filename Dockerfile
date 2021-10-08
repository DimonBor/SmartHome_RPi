FROM python:3.8-buster as builder

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

FROM python:3.8-slim-buster

COPY --from=builder /root/.local /root/.local

COPY . .

CMD [ "python3", "main.py"]
