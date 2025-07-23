from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from fast_zero.settings import Settings

engine = create_engine(
    Settings().DATABASE_URL, connect_args={'check_same_thread': False}
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()
