FROM python:3.12-slim

WORKDIR /app

# Копируем зависимости и устанавливаем их
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем остальной код бэкенда из папки app
COPY ./app ./app
COPY ./run.py .

# Открываем порт для FastAPI
EXPOSE 8000

# Запускаем приложение через run.py (или uvicorn напрямую)
CMD ["python", "run.py"]