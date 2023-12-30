from sqlalchemy import create_engine, MetaData, Table, BigInteger, String, \
    Column, DateTime, ForeignKey, Numeric, SmallInteger

from sqlalchemy.orm import declarative_base
from sqlalchemy.orm import relationship

from datetime import datetime

engine = create_engine("postgresql+psycopg2://postgres:d170303a@localhost/sqlalchemy_tuts")

Base = declarative_base()

class Customer(Base):
    __tablename__ = 'customers'
    id = Column(BigInteger(), primary_key=True)
    first_name = Column(String(100), nullable=False)
    last_name = Column(String(100), nullable=False)
    username = Column(String(50), nullable=False)
    email = Column(String(200), nullable=False)
    created_on = Column(DateTime(), default=datetime.now)
    updated_on = Column(DateTime(), default=datetime.now, onupdate=datetime.now)


Base.metadata.create_all(engine)
