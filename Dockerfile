FROM python:3.12-slim
ENV PYTHONDONTWRITEBYTECODE=1 PYTHONUNBUFFERED=1
WORKDIR /workspace
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && useradd -u 10001 -m appuser && mkdir -p /data && chown appuser:appuser /data
COPY app ./app
USER appuser
ENV DB_PATH=/data/workboard.db
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
