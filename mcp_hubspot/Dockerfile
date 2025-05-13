FROM python:3.11-slim
WORKDIR /app
COPY . .
RUN pip install --no-cache-dir uv && \
    uv pip install -r requirements.txt --system
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "5000"]

