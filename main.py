from fastapi import FastAPI, Request, Depends,  Header, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, SessionLocal
from models import Base, SensorData as DBSensorData
from decision import irrigation_decision

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

latest_decision = "WAIT"


class SensorDataPayload(BaseModel):
    moisture: int
    water_level: float
    pump_status: bool


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.get("/", response_class=HTMLResponse)
def dashboard(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/api/sensor-data")
def receive_data(data: SensorDataPayload, db: Session = Depends(get_db)):
    global latest_decision

    decision = irrigation_decision(data.moisture)
    latest_decision = decision

    new_entry = DBSensorData(
        moisture=data.moisture,
        water_level=data.water_level,
        pump_status=data.pump_status,
        decision=decision
    )

    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)  # Grabs the newly generated ID and Timestamp

    return {"message": "Data saved successfully", "decision": decision}


@app.get("/api/history")
def get_history(limit: int = 50, db: Session = Depends(get_db)):
    data = db.query(DBSensorData)\
        .order_by(DBSensorData.timestamp.desc())\
        .limit(limit)\
        .all()
    return data


@app.get("/api/latest")
def latest_data(db: Session = Depends(get_db)):
    data = db.query(DBSensorData)\
        .order_by(DBSensorData.timestamp.desc())\
        .first()
    return data
