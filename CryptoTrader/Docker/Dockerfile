FROM arm32v7/python:3.8.8-alpine

WORKDIR /app

COPY /app/. /app

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "tradingbot.py"]