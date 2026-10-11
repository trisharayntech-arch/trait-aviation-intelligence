import sqlite3
import os
from pathlib import Path

DB_FILE = Path(__file__).resolve().parent.parent / "trait_aviation.db"

def get_db_connection():
    conn = sqlite3.connect(DB_FILE, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA journal_mode = WAL;")
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # Flights table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS flights (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_number TEXT UNIQUE NOT NULL,
        airline TEXT NOT NULL,
        origin TEXT NOT NULL,
        destination TEXT NOT NULL,
        flight_type TEXT NOT NULL, -- 'Departure' or 'Arrival'
        scheduled_time TEXT NOT NULL,
        estimated_time TEXT NOT NULL,
        actual_time TEXT,
        status TEXT NOT NULL, -- 'On-Time', 'Delayed', 'Boarding', 'Gate Closed', 'Departed', 'Landed', 'Baggage Claim'
        terminal TEXT NOT NULL,
        gate TEXT NOT NULL,
        checkin_desks TEXT NOT NULL,
        baggage_carousel TEXT NOT NULL,
        delay_minutes INTEGER DEFAULT 0,
        delay_reason TEXT DEFAULT 'None', -- 'Carrier', 'Weather', 'NAS/ATC', 'Late Aircraft', 'Security', 'None'
        aircraft_type TEXT NOT NULL,
        passengers_booked INTEGER NOT NULL,
        turnaround_time_mins INTEGER NOT NULL,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)

    # Facilities & Terminals
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS terminals_facilities (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        terminal TEXT NOT NULL,
        category TEXT NOT NULL, -- 'Gate', 'Lounge', 'Security', 'Baggage', 'CheckIn', 'Food', 'Medical', 'Restroom', 'Transit'
        name TEXT NOT NULL,
        location_desc TEXT NOT NULL,
        level TEXT NOT NULL,
        walking_time_mins INTEGER NOT NULL,
        wheelchair_accessible BOOLEAN NOT NULL DEFAULT 1,
        opening_hours TEXT NOT NULL,
        amenities TEXT
    );
    """)

    # Passenger Hourly Flow
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS passenger_hourly_flow (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        terminal TEXT NOT NULL,
        inbound_passengers INTEGER NOT NULL,
        outbound_passengers INTEGER NOT NULL,
        security_wait_mins REAL NOT NULL,
        capacity_pct REAL NOT NULL
    );
    """)

    # Baggage Operations
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS baggage_operations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        flight_number TEXT NOT NULL,
        carousel_id TEXT NOT NULL,
        terminal TEXT NOT NULL,
        total_bags INTEGER NOT NULL,
        processed_bags INTEGER NOT NULL,
        first_bag_mins INTEGER NOT NULL,
        last_bag_mins INTEGER NOT NULL,
        dwell_time_mins INTEGER NOT NULL,
        mishandled_bags INTEGER NOT NULL DEFAULT 0,
        status TEXT NOT NULL -- 'Processing', 'Delivered', 'Delayed Hold', 'Completed'
    );
    """)

    # FAQs & Multilingual Knowledge Base
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faqs_knowledge (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        topic TEXT NOT NULL,
        category TEXT NOT NULL,
        question_en TEXT NOT NULL,
        question_hi TEXT NOT NULL,
        question_es TEXT NOT NULL,
        question_fr TEXT NOT NULL,
        question_de TEXT NOT NULL,
        question_ar TEXT NOT NULL,
        answer_en TEXT NOT NULL,
        answer_hi TEXT NOT NULL,
        answer_es TEXT NOT NULL,
        answer_fr TEXT NOT NULL,
        answer_de TEXT NOT NULL,
        answer_ar TEXT NOT NULL,
        keywords TEXT NOT NULL
    );
    """)

    # Operational Anomalies
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS operational_anomalies (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT NOT NULL,
        incident_type TEXT NOT NULL, -- 'Turnaround Delay', 'Baggage Carousel Jam', 'Security Surge', 'ATC Ground Hold'
        flight_number TEXT,
        location TEXT NOT NULL,
        metric_name TEXT NOT NULL,
        observed_value REAL NOT NULL,
        expected_range TEXT NOT NULL,
        severity TEXT NOT NULL, -- 'HIGH', 'MEDIUM', 'LOW'
        description TEXT NOT NULL,
        status TEXT NOT NULL DEFAULT 'ACTIVE' -- 'ACTIVE', 'RESOLVING', 'RESOLVED'
    );
    """)

    conn.commit()
    conn.close()
    return DB_FILE

if __name__ == "__main__":
    init_db()
    print("Database initialized successfully at:", DB_FILE)
