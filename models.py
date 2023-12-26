from sqlalchemy import create_engine, Column, Integer, String, Date, Float, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship

Base = declarative_base()

class Ship(Base):
    __tablename__ = 'ships'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    displacement = Column(Float)
    port_of_registry = Column(String)
    ship_type = Column(String)
    captain = Column(String)
    visits = relationship("Visit", back_populates="ship")

class Visit(Base):
    __tablename__ = 'visits'
    id = Column(Integer, primary_key=True)
    ship_id = Column(Integer, ForeignKey('ships.id'))
    port_id = Column(Integer, ForeignKey('ports.id'))
    date_of_arrival = Column(Date)
    date_of_departure = Column(Date)
    purpose = Column(String)
    number_of_passengers = Column(Integer)
    ship = relationship("Ship", back_populates="visits")
    port = relationship("Port", back_populates="visits")

class Port(Base):
    __tablename__ = 'ports'
    id = Column(Integer, primary_key=True)
    name = Column(String)
    country = Column(String)
    daily_cost = Column(Float)
    category = Column(String)
    visits = relationship("Visit", back_populates="port")

# Create an engine that stores data in the local directory's
# database file. You can change the database URI as needed.
engine = create_engine('sqlite:///your_database.db')

# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)
