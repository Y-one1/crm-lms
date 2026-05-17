import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Загружаем .env, если он есть (для локальной разработки)
load_dotenv()

# Сначала пытаемся взять URL из переменных окружения (в Докере прилетит оттуда)
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

# Если переменная пустая (например, запустили локально без Docker и забыли .env),
# ставим дефолтный локальный URL, чтобы ничего не сломалось
if not SQLALCHEMY_DATABASE_URL:
    SQLALCHEMY_DATABASE_URL = "postgresql://tutor_user:super_secret_password@localhost:5432/tutor_crm"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Зависимость для получения сессии в FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()