FROM python:3.10-slim

RUN apt-get update && apt-get install -y tor && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

COPY torrc /etc/tor/torrc

EXPOSE 9050 9051

CMD tor & sleep 5 && python examples/example_usage.py
