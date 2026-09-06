# 🚦 SmartGate AI --Integrated-Traffic-City-Management-Control-Center

### 🌟 Next-Gen Integrated Traffic Management & Urban Command Center 🌆

An asynchronous, high-velocity Integrated Command and Control Centre (ICCC) prototype built for Ranchi Smart City Corporation Limited (RSCCL) during the Summer Internship Program 2026.

---

## 📌 Executive Summary

Conventional city traffic lights run on **static countdown timers**, meaning green lights glow for empty lanes while dense queues remain blocked. At the same time, emergency responders like ambulances and fire engines get trapped in gridlock, and traffic rule violations go unpenalized without manual police presence.

**SmartGate AI** bridges physical on-ground intersections directly to a central **Command & Control Room**:

* 🔄 **Dynamic Signal Cycling:** Replaces rigid timers with non-blocking, asynchronous signal state rotations.
* 🚑 **Instant Green Corridor:** Clears emergency routes instantly by forcing conflicting lanes to red and priority lanes to green.
* 📋 **Automated Violation Logs:** Records red-light breaches, stores vehicle numbers, and calculates penalty amounts automatically.
* 📲 **Sub-Second Telegram Push:** Automatically broadcasts accident logs, severity tags, and coordinates directly to on-ground response teams.
* 🚨 **Zero-Dependency Siren:** Synthesizes directional emergency audio alarms directly in the operator browser console.

---

## ✨ Core Features & Functionality

* 🖥️ **Master ICCC Dashboard:** A unified command console displaying a multi-junction visual matrix, countdown timers, violation counts, and active emergency alerts in real time.
* ⏱️ **Asynchronous Signal Engine:** Background workers manage signal phases (`RED` 🔴, `YELLOW` 🟡, `GREEN` 🟢) smoothly without freezing the user interface.
* 🚑 **Emergency Vehicle Preemption:** A priority corridor trigger that clears path blockages for life-saving transit with a single action.
* 📝 **Violation & Fine Tracking:** Persistent recording of vehicle registration numbers, violation categories, and penalty dues for transparent city enforcement.
* 📲 **Telegram Incident Bot:** Direct integration with the Telegram Bot API to dispatch critical accident reports to field personnel in milliseconds.
* 🔊 **In-Console Siren Generator:** Uses the browser's native Web Audio API to produce emergency siren frequencies without needing external MP3/WAV files.
* 📹 **Camera & AI Ready:** Pre-configured architecture to support authenticated RTSP surveillance feeds, vehicle density estimation, and Automatic Number Plate Recognition (ANPR).

---

## 🛠️ Technology Stack Deep Dive

* ⚙️ **Backend Framework (FastAPI):** High-performance Python backend utilizing asynchronous event loops (`async`/`await`) to run background signal timers and process data requests concurrently.
* 📦 **Database Engine (SQLite & SQLAlchemy ORM):** A zero-configuration relational store that manages structured database models for junctions, violations, emergency events, and accident logs.
* 🎨 **Frontend Architecture (HTML5 & CSS3):** A high-contrast, cyber-dark theme engineered specifically for 24/7 operator visibility in traffic control rooms.
* ⚡ **Client-Side Engine (Vanilla JavaScript):** Handles real-time telemetry polling, dynamic DOM updates for signal counters, and the Web Audio API siren generator.
* 🤖 **Dispatch Integration (Telegram Bot API):** Acts as an external communication bridge, sending automated emergency payloads to emergency response groups.
* 📹 **Streaming Protocol (RTSP / ONVIF):** Standard communication standard for integrating physical smart city surveillance cameras.

---

## 🏛️ System Architecture & Data Flow

1. **Junction & Sensor Layer:** On-ground traffic nodes and physical IP cameras stream real-time visual and sensor feeds.
2. **Edge Processing Layer:** Computer vision models analyze lane density, detect collisions, and extract vehicle license plates.
3. **Central API Core (FastAPI):** Processes incoming telemetry, updates signal cycle timing loops, and handles data validation.
4. **Relational Persistence (SQLite):** Writes transaction records for active signals, generated fines, and emergency overrides.
5. **Operator Control Room:** Displays live matrix telemetry and triggers native audio alarms for high-priority incidents.
6. **Field Response:** The Telegram bot pushes coordinates and incident summaries directly to on-ground police and paramedic units.

---

## 🗄️ Database Architecture Overview

* 🚦 **Junctions:** Tracks junction names, geographical coordinates, active light colors, and default cycle timing parameters.
* 🎫 **Violations:** Stores vehicle registration numbers, junction IDs, timestamps, infraction categories (e.g., Red Light Jump), and penalty amounts.
* 🚑 **Emergency Events:** Records priority vehicle classifications (Ambulance/Fire Unit), affected junction corridors, and override activation timestamps.
* ⚠️ **Incident Logs:** Logs accident severity levels, junction locations, operator clearance notes, and Telegram dispatch delivery statuses.
* 📹 **Camera Nodes:** Maintains junction-linked camera IP addresses, port configurations, and authenticated RTSP stream URLs.

---

## 🖥️ Control Room Operator Workflow

* **Step 1 (System Access):** The operator accesses the secure command dashboard and clicks the initialization banner to enable browser audio context for alert sirens.
* **Step 2 (Traffic Monitoring):** The operator observes real-time signal cycles, countdown timers, and vehicle densities across all city intersections.
* **Step 3 (Emergency Preemption):** When an approaching emergency vehicle is verified, the operator activates the **Emergency Corridor**, forcing conflicting signals to red and locking the emergency lane to green.
* **Step 4 (Incident Response):** Upon receiving an accident alert, the dashboard flashes, the audio siren sounds, and an automated Telegram alert is dispatched to field officers. The operator reviews the incident and mutes the alarm.
* **Step 5 (Violation Management):** The system automatically logs red-light jumpers into the penalty records, allowing operators to review logs and generate reports.

---

## 📹 Future Scope: Real-World IP Camera & Edge AI Integration

* 🔐 **Authenticated RTSP Streaming:** Direct integration with standard traffic cameras (Hikvision, Dahua, CP Plus, Axis) using credentials, camera IPs, and port configurations to view feeds in the control room.
* 🧠 **YOLO-Based Density Detection:** Real-time object detection models to count vehicles per lane and adapt green light durations dynamically based on traffic volume.
* 🔍 **Automatic Number Plate Recognition (ANPR):** Automated cropping of vehicles crossing stop lines on red signals, using OCR models to extract license numbers and issue e-challans instantly.
* 💥 **Autonomous Accident Detection:** Spatial tracking models that detect sudden vehicle deceleration or collisions to trigger sirens and Telegram alerts automatically without human delay.
* ⚡ **Edge Compute Deployment:** Deploying lightweight AI models on edge hardware (such as NVIDIA Jetson) at individual junctions to keep bandwidth usage minimal while keeping central governance coordinated.

---

## 👥 Project Credits & Attribution

Developed as an applied engineering project during the **Summer Internship Program 2026** (25 June 2026 – 25 August 2026):

* 💻 Riya Nayak — *B.Tech Data Science & Artificial Intelligence, ICFAI University Jharkhand*

* 💻 Pari Chourasia — *B.Tech Computer Science & Engineering, ICFAI University Jharkhand*

* 🏛️ **Host Organization:** Ranchi Smart City Corporation Limited (RSCCL)
