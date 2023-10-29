from fastapi import FastAPI
from sqlalchemy.orm import Session
from functions.create_plant import create_plant
from reports.plant_list_report import PlantListReport
from main import SessionLocal, app

@app.post("/plants/")
def create_plant_endpoint(land_id: int, flavor_id: int):
    session = SessionLocal()
    plant = create_plant(session, land_id, flavor_id)
    return plant

@app.get("/reports/plant_list/")
def plant_list_report_endpoint():
    session = SessionLocal()
    report = PlantListReport(session)
    report_items = report.run()
    return report_items