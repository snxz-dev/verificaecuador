FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY install_ocr.sh .
RUN bash install_ocr.sh

COPY . .

CMD ["python", "-m", "app.main"]
