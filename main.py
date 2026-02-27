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

@app.get("/api/patients")
def get_patients():
    conn = psycopg2.connect(DATABASE_URL)
    cur = conn.cursor()

    cur.execute("""
        SELECT patient_id,
               predicted_hr,
               predicted_spo2,
               predicted_bp_sys,
               predicted_bp_dys,
               predicted_temp,
               predicted_br,
               created_at
        FROM patients
        ORDER BY created_at DESC
        LIMIT 100
    """)

    rows = cur.fetchall()
    conn.close()

    return [
        {
            "patient_id": r[0],
            "predicted_hr": r[1],
            "predicted_spo2": r[2],
            "predicted_bp_sys": r[3],
            "predicted_bp_dys": r[4],
            "predicted_temp": r[5],
            "predicted_br": r[6],
            "created_at": r[7]
        }
        for r in rows
    ]
