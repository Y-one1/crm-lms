version: '3.8'

services:
  # 1. База данных PostgreSQL
  db:
    image: postgres:15-alpine
    container_name: tutor_crm_db
    restart: always
    environment:
      POSTGRES_USER: tutor_user
      POSTGRES_PASSWORD: super_secret_password
      POSTGRES_DB: tutor_crm
    ports:
      - "5432:5432"
    volumes:
      - pgdata:/var/lib/postgresql/data

  # 2. Бэкенд (FastAPI)
  backend:
    build: ./backend
    container_name: tutor_crm_backend
    restart: always
    ports:
      - "8000:8000"
    environment:
      # Важно: вместо localhost пишем имя сервиса базы данных — db
      DATABASE_URL: postgresql://tutor_user:super_secret_password@db:5432/tutor_crm
    depends_on:
      - db

  # 3. Фронтенд (Vue)
  frontend:
    build: ./frontend
    container_name: tutor_crm_frontend
    restart: always
    ports:
      - "5173:5173"
    depends_on:
      - backend

volumes:
  pgdata: