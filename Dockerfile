FROM python:3.12-slim

WORKDIR /app

# Встановлюємо залежності системи
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Копіюємо requirements
COPY requirements.txt .

# Встановлюємо Python залежності
RUN pip install --no-cache-dir -r requirements.txt

# Копіюємо весь код
COPY . .

# Запускаємо бота
CMD ["python", "-m", "app.main"]
