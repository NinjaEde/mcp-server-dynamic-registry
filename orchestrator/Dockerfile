FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y curl
COPY . .
RUN pip install --no-cache-dir uv && \
    uv pip install -r requirements.txt --system
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

