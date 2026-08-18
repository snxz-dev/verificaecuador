FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt \
    && pip install --no-cache-dir --no-deps rapidocr-onnxruntime==1.2.3

COPY . .

CMD ["python", "-m", "app.main"]
