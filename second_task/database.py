import logging
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from config import DB_HOST, DB_NAME, DB_PASS, DB_PORT, DB_USER

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Формирование URL базы данных
try:
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    logging.info("URL базы данных успешно сформирован.")
except Exception as e:
    logging.error(f"Ошибка при формировании URL базы данных: {e}")
    raise

# Создание базы данных
try:
    engine = create_engine(DATABASE_URL, pool_pre_ping=True)
    logging.info("Движок базы данных успешно создан.")
except Exception as e:
    logging.error(f"Ошибка при создании движка базы данных: {e}")
    raise

# Создание сессии
try:
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    logging.info("SessionLocal успешно создан.")
except Exception as e:
    logging.error(f"Ошибка при создании SessionLocal: {e}")
    raise

# Создание базового класса для моделей
Base = declarative_base()

# Функция для получения сессии


def get_db():
    logging.info("Создание сессии базы данных.")
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logging.error(f"Ошибка во время работы с сессией базы данных: {e}")
        raise
    finally:
        db.close()
        logging.info("Сессия базы данных закрыта.")
