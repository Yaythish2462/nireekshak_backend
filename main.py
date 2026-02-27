from fastapi import FastAPI
from pydantic import BaseModel
import psycopg2
import os

app = FastAPI()

DATABASE_URL = os.getenv("DATABASE_URL")

class Patient(BaseModel):
    patient_id: str
    age: int
    height: float
    weight: float
    gender: int
    predicted_hr: int | None = None
    predicted_spo2: int | None = None
    predicted_bp_sys: int | None = None
    predicted_bp_dys: int | None = None
    predicted_temp: float | None = None
    predicted_br: int | None = None
    face_skintone: str | None = ""
    remarks: str | None = ""

@app.post("/api/patient")
def save_patient(p: Patient):
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("""
        INSERT INTO patients (
            patient_id, age, height, weight, gender,
            predicted_hr, predicted_spo2,
            predicted_bp_sys, predicted_bp_dys,
            predicted_temp, predicted_br,
            face_skintone, remarks
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        p.patient_id, p.age, p.height, p.weight, p.gender,
        p.predicted_hr, p.predicted_spo2,
        p.predicted_bp_sys, p.predicted_bp_dys,
        p.predicted_temp, p.predicted_br,
        p.face_skintone, p.remarks
    ))

    conn.commit()
    conn.close()
    return {"status": "saved"}