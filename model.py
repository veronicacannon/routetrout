from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine, ForeignKey
from sqlalchemy import Column, Integer, String, DateTime, Date, Boolean

from sqlalchemy.orm import sessionmaker, scoped_session, relationship, backref
import os

db_uri = os.environ.get("DATABASE_URL", "sqlite:///rt.db")
    
engine = create_engine(db_uri, echo=False) 
session = scoped_session(sessionmaker(bind=engine,
                         autocommit = False,
                         autoflush = False))

Base = declarative_base()
Base.query = session.query_property

class Health_Alert(Base):
    __tablename__ = "health_alerts"
    id = Column(Integer, primary_key = True)
    description = Column(String(128), nullable=False)
    status = Column(String(256))

class Participant(Base):
    __tablename__ = "participants"

    # status
    id = Column(Integer, primary_key = True)
    full_name = Column(String(128), nullable=False)
    status = Column(String(256))
    route = Column(String(60))
    Q_ID = Column(String(60))
    general_notes = Column(String(256))

    # contact
    lang_english = Column(Boolean(create_constraint=True, name=None))
    lang_interpreter = Column(String(60))
    mail_addr_line1 = Column(String(80))
    mail_addr_line2 = Column(String(80))
    mail_addr_city = Column(String(80))
    mail_addr_state = Column(String(2))
    mail_addr_zipcode = Column(String(12))
    tel_1 = Column(String(20))
    tel_2 = Column(String(20))
    email_1 = Column(String(60))  

def create_db():
    Base.metadata.create_all(engine)

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
