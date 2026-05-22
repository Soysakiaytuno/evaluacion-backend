FROM python:3.11-slim
WORKDIR /app
RUN groupadd -r web && useradd -r -g web web
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt
COPY --chown=web:web . /app/
USER web