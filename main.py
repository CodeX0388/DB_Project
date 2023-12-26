from fastapi import FastAPI, HTTPException
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from pydantic import BaseModel

app = FastAPI()

DATABASE_URL = "postgresql://user:password@localhost/dbname"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

# Define the Ship model
class Ship(Base):
    __tablename__ = 'ships'
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    displacement = Column(Float)
    port_of_registry = Column(String)
    type = Column(String)
    captain = Column(String)

Base.metadata.create_all(bind=engine)

# Pydantic models for request and response data
class ShipCreate(BaseModel):
    name: str
    displacement: float
    port_of_registry: str
    type: str
    captain: str

class ShipResponse(ShipCreate):
    id: int

    class Config:
        orm_mode = True

# CRUD operations
@app.post("/ships/", response_model=ShipResponse)
def create_ship(ship: ShipCreate, db: Session = Depends(SessionLocal)):
    db_ship = Ship(**ship.dict())
    db.add(db_ship)
    db.commit()
    db.refresh(db_ship)
    return db_ship

@app.get("/ships/{ship_id}", response_model=ShipResponse)
def read_ship(ship_id: int, db: Session = Depends(SessionLocal)):
    db_ship = db.query(Ship).filter(Ship.id == ship_id).first()
    if db_ship is None:
        raise HTTPException(status_code=404, detail="Ship not found")
    return db_ship

@app.put("/ships/{ship_id}", response_model=ShipResponse)
def update_ship(ship_id: int, ship: ShipCreate, db: Session = Depends(SessionLocal)):
    db_ship = db.query(Ship).filter(Ship.id == ship_id).first()
    if db_ship is None:
        raise HTTPException(status_code=404, detail="Ship not found")
    for var, value in vars(ship).items():
        setattr(db_ship, var, value) if value else None
    db.commit()
    return db_ship

@app.delete("/ships/{ship_id}")
def delete_ship(ship_id: int, db: Session = Depends(SessionLocal)):
    db_ship = db.query(Ship).filter(Ship.id == ship_id).first()
    if db_ship is None:
        raise HTTPException(status_code=404, detail="Ship not found")
    db.delete(db_ship)
    db.commit()
    return {"ok": True}



# API endpoints
@app.get("/ships/")
def read_ships(type: str, min_displacement: float, db: Session = Depends(get_db)):
    ships = db.query(Ship).filter(Ship.type == type, Ship.displacement >= min_displacement).all()
    return ships

@app.get("/visits/join/")
def read_visits_with_ships(db: Session = Depends(get_db)):
    visits = db.query(Visit).options(joinedload(Visit.ship)).all()
    return visits

@app.put("/ships/update/")
def update_ship(captain: str, new_type: str, db: Session = Depends(get_db)):
    db.query(Ship).filter(Ship.captain == captain).update({"type": new_type})
    db.commit()
    return {"message": "Ships updated"}

@app.get("/ports/group-by/")
def group_ports_by_country(db: Session = Depends(get_db)):
    ports = db.query(Port.country, func.count(Port.id)).group_by(Port.country).all()
    return ports

@app.get("/ships/subquery/")
def read_ships_with_max_displacement(db: Session = Depends(get_db)):
    max_displacement = db.query(func.max(Ship.displacement)).scalar()
    ships = db.query(Ship).filter(Ship.displacement == max_displacement).all()
    return ships
