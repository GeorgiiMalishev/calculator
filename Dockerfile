# Используйте официальный образ Python с Docker Hub
FROM python:3.9-slim

# Установите переменные окружения
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Установите рабочую директорию
WORKDIR /app

# Скопируйте файл зависимостей
COPY requirements.txt /app/

# Установите зависимости
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Скопируйте файлы проекта
COPY . /app/

# Откройте порт, на котором работает приложение
EXPOSE 8000

# Запустите приложение
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
