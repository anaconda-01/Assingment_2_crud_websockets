from sqlalchemy import create_engine,text
from sqlalchemy.orm import sessionmaker

url = 'postgresql://postgres:root@localhost:5432/users'
engine = create_engine(url)
def get_db():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        print(e)
        db.rollback()
        raise
    finally:
        db.close()
def create_table(Base):
    try:
        Base.metadata.create_all(bind=engine)
        return "created all the tables"
    except Exception as e:
        return f"{e}"



