import sqlalchemy
from sqlalchemy.orm import sessionmaker

DNS = 'postgresql://postgres:12345@localhost:5432/sqlalchemy_db'
engine = sqlalchemy.create_engine(DNS)

Session = sessionmaker(bind=engine)
session = Session()






session.close()