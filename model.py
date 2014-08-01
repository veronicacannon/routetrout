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

#
#   PREFERENCES
#
class Preferences(Base):
    __tablename__ = "preferences"
    id = Column(Integer, primary_key = True)
    description = Column(String(128), nullable=False)

#
#   PARTICIPANT
#
class Participant(Base):
    __tablename__ = "participants"

    # status
    id = Column(Integer, primary_key = True)
    full_name = Column(String(128), nullable=False)
    ptype = Column(String(128), nullable=False)    # participant type
    status = Column(String(20), default="")
    route = Column(String(60), default="")
    Q_ID = Column(String(60), default="")
    general_notes = Column(String(256), default="")

    # delivery
    delivery_addr_line1 = Column(String(80), default="")
    delivery_addr_line2 = Column(String(80), default="")
    delivery_city = Column(String(80), default="")
    delivery_state = Column(String(2), default="")
    delivery_zipcode = Column(String(12), default="")
    delivery_county = Column(String(20), default="")
    tel_3 = Column(String(20), default="")
    delivery_notes = Column(String(256), default="")

    # contact
    lang_english = Column(Boolean, unique=False, default=True)
    lang_interpreter = Column(String(60), default="")
    mail_addr_line1 = Column(String(80), default="")
    mail_addr_line2 = Column(String(80), default="")
    mail_city = Column(String(80), default="")
    mail_state = Column(String(2), default="")
    mail_zipcode = Column(String(12), default="")
    email_1 = Column(String(60), default="")  
    tel_1 = Column(String(20), default="")
    tel_2 = Column(String(20), default="")

    # vitals
    SSN_4 = Column(String(4), default="")
    birthdate = Column(Date)
    gender = Column(String(1), default="")
    martial_status = Column(String(20), default="")
    living_status = Column(String(60), default="")
    household = Column(String(20), default="")
    female_head = Column(Boolean, unique=False, default=False)
    rent_own = Column(String(10), default="")
    rural_status = Column(String(20), default="")
    migrant_farm_worker = Column(Boolean, unique=False, default=False)
    poverty_status = Column(String(20), default="")
    income_level = Column(String(40), default="")
    completed_ed = Column(String(40), default="")    
    race = Column(String(40), default="")
    ethnicity = Column(String(40), default="")
    disabled = Column(Boolean, unique=False, default=False)
    healthcare = Column(String(60), default="")

#
#   PARTICIPANT PREFERENCES
#
class Participant_Preferences(Base):
    __tablename__ = "part_prefs"

    id = Column(Integer, primary_key = True)
    participant_id = Column(Integer, ForeignKey('participants.id')) 
    pref_type = Column (String(20)) # alert, yes, no
    pref_description = Column(String(128), nullable=False)

    participant = relationship("Participant", backref="part_pref")

#
#   PARTICIPANT MEALS
#
class Participant_Meals(Base):
    __tablename__ = "part_meals"

    id = Column(Integer, primary_key = True)
    participant_id = Column(Integer, ForeignKey('participants.id')) 
    delivery_day = Column(String(3))
    meal_type = Column(String(10))
    qty = Column(Integer)

    participant = relationship("Participant", backref="part_meals")

#
#   ROUTE
#
class Route_Details(Base):
    __tablename__ = "route_details"

    id = Column(Integer, primary_key = True)
    route_date = Column(Date)
    route = Column(String(60))
    participant_id = Column(Integer, ForeignKey('participants.id'))
    regular = Column(Integer)
    frozen = Column(Integer)
    breakfast = Column(Integer)
    milk = Column(Integer)
    salad = Column(Integer)
    fruit = Column(Integer)
    bread = Column(Integer)

    participant = relationship("Participant", backref="route_details")

def create_db():
    Base.metadata.create_all(engine)

def main():
    """In case we need this for something"""
    pass

if __name__ == "__main__":
    main()
