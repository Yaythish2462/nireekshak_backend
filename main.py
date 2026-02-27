from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import os
from typing import Optional

# -------------------------------------------------
# App Initialization
# -------------------------------------------------

app = FastAPI()

# -------------------------------------------------
# CORS Configuration (IMPORTANT)
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # For development. Later restrict to Netlify URL.
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Database Configuration
# -------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set in environment variables")

# -------------------------------------------------
# Pydantic Model
# -------------------------------------------------

class Patient(BaseModel):
    patient_id: str
    age: int
    height: float
    weight: float
    gender: int
    predicted_hr: Optional[int] = None
    predicted_spo2: Optional[int] = None
    predicted_bp_sys: Optional[int] = None
    predicted_bp_dys: Optional[int] = None
    predicted_temp: Optional[float] = None
    predicted_br: Optional[int] = None
    face_skintone: Optional[str] = ""
    remarks: Optional[str] = ""

# -------------------------------------------------
# Root Endpoint (Health Check)
# -------------------------------------------------

@app.get("/")
def health_check():
    return {"status": "Nireekshak API running"}

# -------------------------------------------------
# Insert Patient Data
# -------------------------------------------------

@app.post("/api/patient")
def save_patient(p: Patient):
    try:
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO patients (
                patient_id, age, height, weight, gender,
                predicted_hr, predicted_spo2,
                predicted_bp_sys, predicted_bp_dys,
                predicted_temp, predicted_br,
                face_skintone, remarks
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (
            p.patient_id, p.age, p.height, p.weight, p.gender,
            p.predicted_hr, p.predicted_spo2,
            p.predicted_bp_sys, p.predicted_bp_dys,
            p.predicted_temp, p.predicted_br,
            p.face_skintone, p.remarks
        ))

        conn.commit()
        cur.close()
        conn.close()

        return {"status": "saved"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# -------------------------------------------------
# Fetch Latest Patients
# -------------------------------------------------

@app.get("/api/patients")
def get_patients():
    try:
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
        cur.close()
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

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
