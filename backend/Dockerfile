FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY install.sh .
RUN bash install.sh

COPY . .

CMD ["python", "-m", "app.main"]
