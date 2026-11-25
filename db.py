import sqlite3
import json
from pathlib import Path

DB_PATH = Path(__file__).parent / "job_agent.db"


def init_db():
    """Create db"""
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS candidates (
                id               INTEGER PRIMARY KEY AUTOINCREMENT,
                name             TEXT NOT NULL,
                resume_filename  TEXT UNIQUE NOT NULL,
                profile_json     TEXT NOT NULL,
                created_at       TEXT DEFAULT CURRENT_TIMESTAMP,
                updated_at       TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)

        conn.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
            id          INTEGER PRIMARY KEY AUTOINCREMENT,
            title       TEXT NOT NULL,
            company     TEXT,
            location    TEXT,
            description TEXT,
            job_url     TEXT UNIQUE NOT NULL,
            source      TEXT,
            discovered_at TEXT DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.commit()

    finally:
        conn.close()


def save_candidate(profile, resume_filename):
    profile_json = json.dumps(profile)
    conn = sqlite3.connect(DB_PATH)
    try:
        conn.execute("""
            INSERT INTO candidates (
                name,
                resume_filename,
                profile_json
            )
            VALUES (?, ?, ?)

            ON CONFLICT(resume_filename)
            DO UPDATE SET
                name = excluded.name,
                profile_json = excluded.profile_json,
                updated_at = CURRENT_TIMESTAMP
        """, (
            profile["name"],
            resume_filename,
            profile_json
        )
        )

        conn.commit()

        cursor = conn.execute(
            "SELECT id FROM candidates WHERE resume_filename = ?",
            (resume_filename,)
        )

        return cursor.fetchone()[0]

    finally:
        conn.close()


def get_candidate(resume_filename):
    """Retrieve a saved candidate profile."""

    conn = sqlite3.connect(DB_PATH)

    try:
        cursor = conn.execute("""
            SELECT id, name, resume_filename, profile_json,
                   created_at, updated_at
            FROM candidates
            WHERE resume_filename = ?
        """, (resume_filename,))

        row = cursor.fetchone()

        if row is None:
            return None

        return {
            "id": row[0],
            "name": row[1],
            "resume_filename": row[2],
            "profile": json.loads(row[3]),
            "created_at": row[4],
            "updated_at": row[5]
        }

    finally:
        conn.close()


def save_jobs(jobs):
    conn = sqlite3.connect(DB_PATH)
    saved_count = 0

    try:
        for job in jobs:
            cursor = conn.execute("""
                INSERT OR IGNORE INTO jobs (
                    title, company, location,
                    description, job_url, source
                )
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                job.get("title"),
                job.get("company"),
                job.get("location"),
                job.get("description"),
                job.get("job_url"),
                job.get("source", "Unknown")
            ))

            saved_count += cursor.rowcount

        conn.commit()
        return saved_count

    finally:
        conn.close()


def get_saved_jobs():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row

    try:
        cursor = conn.execute("""
            SELECT *
            FROM jobs
            ORDER BY discovered_at DESC
        """)

        return [dict(row) for row in cursor.fetchall()]

    finally:
        conn.close()
