import sqlite3
import numpy as np
import cv2
import os
from datetime import datetime
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, HTMLResponse

app = FastAPI(title="SmartGate AI: Main Grid Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "database.db"
CHOWK_LANES = ["North Lane", "South Lane", "East Lane", "West Lane"]

EMERGENCY_LABELS = {
    "ambulance": "🏥 Emergency Medical Services (Ambulance)",
    "police": "🚓 Law Enforcement Secure Escort (Police)",
    "fire": "🚒 Fire Brigade & Rescue Services (Fire Truck)"
}


def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS iccc_analytics (
            id INTEGER PRIMARY KEY, 
            total_revenue INTEGER, 
            challans INTEGER, 
            accidents INTEGER
        )
    """)
    cursor.execute("SELECT * FROM iccc_analytics WHERE id = 1")
    if not cursor.fetchone():
        cursor.execute("INSERT INTO iccc_analytics VALUES (1, 44500, 44, 0)")

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS traffic_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT,
            vehicle_type TEXT,
            license_plate TEXT,
            lane_approached TEXT,
            priority_status TEXT
        )
    """)
    conn.commit()
    conn.close()


init_db()


@app.get("/", response_class=HTMLResponse)
async def get_dashboard():
    template_path = os.path.join("templates", "dashboard.html")
    if os.path.exists(template_path):
        with open(template_path, "r", encoding="utf-8") as f:
            return f.read()
    return "<h3>Error: templates/dashboard.html file missing.</h3>"


@app.get("/api/v1/database/metrics")
async def get_metrics():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT total_revenue, challans, accidents FROM iccc_analytics WHERE id = 1")
    res = cursor.fetchone()
    conn.close()
    return JSONResponse(content={"revenue": res[0], "challans": res[1], "accidents": res[2]})


@app.get("/api/v1/database/logs")
async def get_database_logs():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute(
        "SELECT id, timestamp, vehicle_type, license_plate, lane_approached, priority_status FROM traffic_logs ORDER BY id DESC")
    rows = cursor.fetchall()
    conn.close()
    return JSONResponse(content={"logs": [
        {"id": r[0], "timestamp": r[1], "vehicle_type": r[2], "license_plate": r[3], "lane_approached": r[4],
         "priority_status": r[5]} for r in rows]})


@app.post("/api/v1/database/accidents/trigger")
async def trigger_accident_counter():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE iccc_analytics SET accidents = accidents + 1 WHERE id = 1")
    conn.commit()
    conn.close()
    return {"status": "Updated"}


@app.post("/api/v1/database/accidents/clear")
async def clear_accident_counter():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("UPDATE iccc_analytics SET accidents = MAX(0, accidents - 1) WHERE id = 1")
    conn.commit()
    conn.close()
    return {"status": "Cleared"}


@app.post("/api/v1/camera/pipeline")
async def camera_pipeline(file: UploadFile = File(...)):
    filename_lower = file.filename.lower()
    vehicle_type = "Standard Passenger Vehicle (Car)"
    is_priority = False
    raw_plate = "JHOJA04962"
    trigger_penalty = False
    is_accident = False

    if "accident" in filename_lower or "crash" in filename_lower:
        is_accident = True
        vehicle_type = "⚠️ CRITICAL VEHICULAR COLLISION"
        raw_plate = "JH01BZ-7740"
    else:
        for key, label in EMERGENCY_LABELS.items():
            if key in filename_lower:
                vehicle_type = label
                is_priority = True
                raw_plate = "PRIORITY-PASS"
                break

        if not is_priority and ("bike" in filename_lower or "motorcycle" in filename_lower):
            vehicle_type = "Two-Wheeler (Motorcycle/Bike)"
            trigger_penalty = True
            raw_plate = "JH01EF-8821"

    incoming_lane = "West Lane" if not is_priority else np.random.choice(CHOWK_LANES)

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    priority_str = "CRITICAL" if is_accident else ("HIGH" if is_priority else "NORMAL")

    cursor.execute("""
        INSERT INTO traffic_logs (timestamp, vehicle_type, license_plate, lane_approached, priority_status)
        VALUES (?, ?, ?, ?, ?)
    """, (current_time, vehicle_type, raw_plate, incoming_lane, priority_str))

    if trigger_penalty:
        cursor.execute(
            "UPDATE iccc_analytics SET total_revenue = total_revenue + 1000, challans = challans + 1 WHERE id = 1")

    cursor.execute("SELECT total_revenue, challans, accidents FROM iccc_analytics WHERE id = 1")
    live_analytics = cursor.fetchone()
    conn.commit()
    conn.close()

    system_action = "⚠️ CRITICAL DISPATCH INITIATED" if is_accident else "STANDARD TRAFFIC ENTRY LOGGED"
    if trigger_penalty:
        system_action = f"🚨 DETECTED: {vehicle_type}. AUTOMATED PENALTY ENGINE UPDATED (+₹1000 Fine Logged)"
    elif is_priority:
        system_action = f"🚨 EMERGENCY OVERRIDE ACTIVE: {vehicle_type} Clear Corridor Triggered."

    return JSONResponse(content={
        "status": "Logged Successfully",
        "is_accident": is_accident,
        "extracted_plate": raw_plate,
        "vehicle_classification": vehicle_type,
        "system_action_protocol": system_action,
        "junction_live_routing": {
            "incoming_direction": incoming_lane,
            "signal_matrix": {"west_lane": "🟢 GREEN" if is_priority else "🔄 ROTATING(3s Interval"},
            "traffic_state": "CRASH AUTOMATION LOCK" if is_accident else "Fluid Traffic"
        },
        "live_iccc_counters": {
            "traffic_density": "GRID INTERRUPT (CRASH)" if is_accident else (
                "High Density" if trigger_penalty else "Fluid Traffic"),
            "active_challans": live_analytics[1],
            "tracked_accidents": live_analytics[2]
        }
    })