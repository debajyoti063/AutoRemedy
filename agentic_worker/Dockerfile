FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt && pip install redis

COPY . .

ENV REDIS_HOST=redis
ENV REDIS_PORT=6379

CMD ["python", "-m", "agentic_worker.main"] 