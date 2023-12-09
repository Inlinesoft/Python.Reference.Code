import sqlalchemy as sa
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import utilities.database as db

engine = db.create_engine()
Base = declarative_base(engine)

class Log(Base):
    __tablename__ = 'Log'
    __table_args__ = {'autoload': True}

# if __name__ == "__main__":
#     print('From Main')
