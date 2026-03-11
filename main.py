from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import psycopg2
import os
from typing import Optional

# -------------------------------------------------
# FastAPI App
# -------------------------------------------------

app = FastAPI(title="Nireekshak API")

# -------------------------------------------------
# CORS (Allow frontend access e.g., Netlify)
# -------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change later to your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# -------------------------------------------------
# Database
# -------------------------------------------------

DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise RuntimeError("DATABASE_URL not set")


def get_connection():
    return psycopg2.connect(DATABASE_URL, sslmode="require")


# -------------------------------------------------
# Patient Model
# -------------------------------------------------

class Patient(BaseModel):

    patient_id: str
    age: int
    height: float
    weight: float
    gender: int

    heart_rate: Optional[int] = None
    predicted_hr: Optional[int] = None

    breathe_rate: Optional[int] = None
    predicted_breathe_rate: Optional[int] = None

    spo2: Optional[int] = None
    predicted_spo2: Optional[int] = None

    temperature: Optional[float] = None
    predicted_temperature: Optional[float] = None

    bp_sys: Optional[int] = None
    predicted_bp_sys: Optional[int] = None

    bp_dys: Optional[int] = None
    predicted_bp_dys: Optional[int] = None

    face_skintone: Optional[str] = ""
    remarks: Optional[str] = ""


# -------------------------------------------------
# Health Check
# -------------------------------------------------

@app.get("/")
def health():
    return {"status": "Nireekshak API running"}


# -------------------------------------------------
# Insert Patient Data
# -------------------------------------------------

@app.post("/api/patient")
def save_patient(p: Patient):

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        INSERT INTO patients (
            patient_id,
            age,
            height,
            weight,
            gender,
            heart_rate,
            predicted_hr,
            breathe_rate,
            predicted_breathe_rate,
            spo2,
            predicted_spo2,
            temperature,
            predicted_temperature,
            bp_sys,
            predicted_bp_sys,
            bp_dys,
            predicted_bp_dys,
            face_skintone,
            remarks
        )
        VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """,
        (
            p.patient_id,
            p.age,
            p.height,
            p.weight,
            p.gender,
            p.heart_rate,
            p.predicted_hr,
            p.breathe_rate,
            p.predicted_breathe_rate,
            p.spo2,
            p.predicted_spo2,
            p.temperature,
            p.predicted_temperature,
            p.bp_sys,
            p.predicted_bp_sys,
            p.bp_dys,
            p.predicted_bp_dys,
            p.face_skintone,
            p.remarks
        ))

        conn.commit()

        cur.close()
        conn.close()

        return {"status": "saved"}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# -------------------------------------------------
# Get All Patients
# -------------------------------------------------

@app.get("/api/patients")
def get_patients():

    try:
        conn = get_connection()
        cur = conn.cursor()

        cur.execute("""
        SELECT
            id,
            patient_id,
            age,
            height,
            weight,
            gender,
            heart_rate,
            predicted_hr,
            breathe_rate,
            predicted_breathe_rate,
            spo2,
            predicted_spo2,
            temperature,
            predicted_temperature,
            bp_sys,
            predicted_bp_sys,
            bp_dys,
            predicted_bp_dys,
            face_skintone,
            remarks,
            created_at
        FROM patients
        ORDER BY created_at DESC
        """)

        rows = cur.fetchall()

        cur.close()
        conn.close()

        return [
            {
                "id": r[0],
                "patient_id": r[1],
                "age": r[2],
                "height": r[3],
                "weight": r[4],
                "gender": r[5],
                "heart_rate": r[6],
                "predicted_hr": r[7],
                "breathe_rate": r[8],
                "predicted_breathe_rate": r[9],
                "spo2": r[10],
                "predicted_spo2": r[11],
                "temperature": r[12],
                "predicted_temperature": r[13],
                "bp_sys": r[14],
                "predicted_bp_sys": r[15],
                "bp_dys": r[16],
                "predicted_bp_dys": r[17],
                "face_skintone": r[18],
                "remarks": r[19],
                "created_at": r[20]
            }
            for r in rows
        ]

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
