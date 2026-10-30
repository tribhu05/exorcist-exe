import sqlite3
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone

from app.config import settings
from app.models.schemas import GrimoireRecord

logger = logging.getLogger("phantom.grimoire")

class GrimoireStore:
    def __init__(self, db_path: str = settings.DB_PATH):
        self.db_path = db_path
        self._init_db()

    def _get_connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_db(self):
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    CREATE TABLE IF NOT EXISTS incidents (
                        id TEXT PRIMARY KEY,
                        created_at TEXT NOT NULL,
                        incident_type TEXT NOT NULL,
                        title TEXT NOT NULL,
                        severity TEXT NOT NULL,
                        details_json TEXT NOT NULL,
                        resolved INTEGER DEFAULT 0
                    )
                """)
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to initialize Grimoire SQLite database: {e}")

    def record_incident(
        self,
        incident_id: str,
        incident_type: str,
        title: str,
        severity: str,
        details: Dict[str, Any]
    ) -> GrimoireRecord:
        now = datetime.now(timezone.utc).isoformat()
        details_str = json.dumps(details)
        try:
            with self._get_connection() as conn:
                conn.execute("""
                    INSERT OR REPLACE INTO incidents (id, created_at, incident_type, title, severity, details_json, resolved)
                    VALUES (?, ?, ?, ?, ?, ?, 0)
                """, (incident_id, now, incident_type, title, severity, details_str))
                conn.commit()
        except Exception as e:
            logger.error(f"Failed to record incident in Grimoire: {e}")

        return GrimoireRecord(
            id=incident_id,
            created_at=now,
            incident_type=incident_type,
            title=title,
            severity=severity,
            details=details,
            resolved=False
        )

    def list_incidents(self, limit: int = 50) -> List[GrimoireRecord]:
        results = []
        try:
            with self._get_connection() as conn:
                cur = conn.execute("""
                    SELECT id, created_at, incident_type, title, severity, details_json, resolved
                    FROM incidents
                    ORDER BY created_at DESC
                    LIMIT ?
                """, (limit,))
                for row in cur.fetchall():
                    try:
                        details = json.loads(row["details_json"])
                    except Exception:
                        details = {}
                    results.append(GrimoireRecord(
                        id=row["id"],
                        created_at=row["created_at"],
                        incident_type=row["incident_type"],
                        title=row["title"],
                        severity=row["severity"],
                        details=details,
                        resolved=bool(row["resolved"])
                    ))
        except Exception as e:
            logger.error(f"Failed to fetch incidents from Grimoire: {e}")
        return results

    def resolve_incident(self, incident_id: str) -> bool:
        try:
            with self._get_connection() as conn:
                cur = conn.execute("""
                    UPDATE incidents SET resolved = 1 WHERE id = ?
                """, (incident_id,))
                conn.commit()
                return cur.rowcount > 0
        except Exception as e:
            logger.error(f"Failed to resolve incident {incident_id}: {e}")
            return False

    def get_count(self) -> int:
        try:
            with self._get_connection() as conn:
                cur = conn.execute("SELECT COUNT(*) as cnt FROM incidents")
                row = cur.fetchone()
                return row["cnt"] if row else 0
        except Exception:
            return 0

grimoire_store = GrimoireStore()
