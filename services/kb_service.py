import sqlite3
import os
from datetime import datetime
from typing import Dict, List, Optional

from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "database/kb.db")


def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


# ---------------------------------------------------------------------------
# Themes
# ---------------------------------------------------------------------------

def get_all_themes() -> List[Dict]:
    conn = get_db_connection()
    try:
        rows = conn.execute("SELECT * FROM themes ORDER BY name").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def create_theme(name: str, icon: str = "📌") -> Optional[Dict]:
    conn = get_db_connection()
    try:
        if conn.execute("SELECT id FROM themes WHERE name = ?", (name,)).fetchone():
            return None
        cur = conn.execute("INSERT INTO themes (name, icon) VALUES (?, ?)", (name, icon))
        conn.commit()
        row = conn.execute("SELECT * FROM themes WHERE id = ?", (cur.lastrowid,)).fetchone()
        return dict(row)
    finally:
        conn.close()


def get_or_create_theme(conn: sqlite3.Connection, theme_name: str) -> int:
    row = conn.execute("SELECT id FROM themes WHERE name = ?", (theme_name,)).fetchone()
    if row:
        return row["id"]
    cur = conn.execute("INSERT INTO themes (name, icon) VALUES (?, ?)", (theme_name, "📌"))
    conn.commit()
    return cur.lastrowid


# ---------------------------------------------------------------------------
# Types
# ---------------------------------------------------------------------------

def get_all_types() -> List[Dict]:
    conn = get_db_connection()
    try:
        rows = conn.execute("SELECT * FROM types ORDER BY name").fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def create_type(name: str, icon: str = "📄") -> Optional[Dict]:
    conn = get_db_connection()
    try:
        if conn.execute("SELECT id FROM types WHERE name = ?", (name,)).fetchone():
            return None
        cur = conn.execute("INSERT INTO types (name, icon) VALUES (?, ?)", (name, icon))
        conn.commit()
        row = conn.execute("SELECT * FROM types WHERE id = ?", (cur.lastrowid,)).fetchone()
        return dict(row)
    finally:
        conn.close()


def get_or_create_type(conn: sqlite3.Connection, type_name: str) -> int:
    row = conn.execute("SELECT id FROM types WHERE name = ?", (type_name,)).fetchone()
    if row:
        return row["id"]
    cur = conn.execute("INSERT INTO types (name, icon) VALUES (?, ?)", (type_name, "📄"))
    conn.commit()
    return cur.lastrowid


# ---------------------------------------------------------------------------
# Tags
# ---------------------------------------------------------------------------

def get_all_tags() -> List[str]:
    conn = get_db_connection()
    try:
        rows = conn.execute(
            "SELECT tags FROM knowledge_items WHERE tags IS NOT NULL AND tags != ''"
        ).fetchall()
        all_tags: set = set()
        for row in rows:
            for tag in row["tags"].split(","):
                tag = tag.strip()
                if tag:
                    all_tags.add(tag)
        return sorted(all_tags)
    finally:
        conn.close()


# ---------------------------------------------------------------------------
# Knowledge items
# ---------------------------------------------------------------------------

_SELECT_ITEMS = """
    SELECT ki.*,
           th.name AS theme_name, th.icon AS theme_icon,
           ty.name AS type_name,  ty.icon AS type_icon
    FROM   knowledge_items ki
    LEFT JOIN themes th ON ki.theme_id = th.id
    LEFT JOIN types  ty ON ki.type_id  = ty.id
"""


def get_all_knowledge_items() -> List[Dict]:
    conn = get_db_connection()
    try:
        rows = conn.execute(
            _SELECT_ITEMS + " ORDER BY ki.date_modification DESC"
        ).fetchall()
        return [dict(r) for r in rows]
    finally:
        conn.close()


def get_knowledge_item(item_id: int) -> Optional[Dict]:
    conn = get_db_connection()
    try:
        row = conn.execute(
            _SELECT_ITEMS + " WHERE ki.id = ?", (item_id,)
        ).fetchone()
        return dict(row) if row else None
    finally:
        conn.close()


def create_knowledge_item(data: Dict) -> Dict:
    conn = get_db_connection()
    try:
        theme_id = get_or_create_theme(conn, data["theme_name"])
        type_id  = get_or_create_type(conn, data["type_name"])
        now = datetime.utcnow().isoformat()
        cur = conn.execute(
            """INSERT INTO knowledge_items
               (theme_id, type_id, titre, description, code, solution, tags,
                date_creation, date_modification)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            (
                theme_id, type_id,
                data["titre"],
                data.get("description"),
                data.get("code"),
                data.get("solution"),
                data.get("tags"),
                now, now,
            ),
        )
        conn.commit()
        return get_knowledge_item(cur.lastrowid)
    finally:
        conn.close()


def update_knowledge_item(item_id: int, data: Dict) -> Optional[Dict]:
    conn = get_db_connection()
    try:
        if not conn.execute(
            "SELECT id FROM knowledge_items WHERE id = ?", (item_id,)
        ).fetchone():
            return None

        fields: List[str] = []
        values: List = []

        if data.get("theme_name") is not None:
            fields.append("theme_id = ?")
            values.append(get_or_create_theme(conn, data["theme_name"]))

        if data.get("type_name") is not None:
            fields.append("type_id = ?")
            values.append(get_or_create_type(conn, data["type_name"]))

        for col in ("titre", "description", "code", "solution", "tags"):
            if col in data and data[col] is not None:
                fields.append(f"{col} = ?")
                values.append(data[col])

        fields.append("date_modification = ?")
        values.append(datetime.utcnow().isoformat())
        values.append(item_id)

        conn.execute(
            f"UPDATE knowledge_items SET {', '.join(fields)} WHERE id = ?", values
        )
        conn.commit()
        return get_knowledge_item(item_id)
    finally:
        conn.close()


def delete_knowledge_item(item_id: int) -> bool:
    conn = get_db_connection()
    try:
        if not conn.execute(
            "SELECT id FROM knowledge_items WHERE id = ?", (item_id,)
        ).fetchone():
            return False
        conn.execute("DELETE FROM knowledge_items WHERE id = ?", (item_id,))
        conn.commit()
        return True
    finally:
        conn.close()
