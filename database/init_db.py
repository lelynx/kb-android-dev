import sqlite3
import os
from dotenv import load_dotenv

load_dotenv()

DB_PATH = os.getenv("DB_PATH", "database/kb.db")


def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.executescript("""
        CREATE TABLE IF NOT EXISTS themes (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT    NOT NULL UNIQUE,
            icon         TEXT    DEFAULT '📌',
            date_created TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS types (
            id           INTEGER PRIMARY KEY AUTOINCREMENT,
            name         TEXT    NOT NULL UNIQUE,
            icon         TEXT    DEFAULT '📄',
            date_created TEXT    DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS knowledge_items (
            id                INTEGER PRIMARY KEY AUTOINCREMENT,
            theme_id          INTEGER REFERENCES themes(id),
            type_id           INTEGER REFERENCES types(id),
            titre             TEXT    NOT NULL,
            description       TEXT,
            code              TEXT,
            solution          TEXT,
            tags              TEXT,
            date_creation     TEXT    DEFAULT (datetime('now')),
            date_modification TEXT    DEFAULT (datetime('now'))
        );
    """)

    types_seed = [
        (1, "Concept",          "📘"),
        (2, "Snippet",          "💻"),
        (3, "Erreur résolue",   "🐛"),
        (4, "Astuce",           "💡"),
        (5, "Question ouverte", "❓"),
        (6, "Objectif",         "🎯"),
        (7, "Ressource",        "✳️"),
        (8, "Piège",            "⚠️"),
        (9, "Procédure",        "📋"),
    ]
    for row in types_seed:
        cursor.execute(
            "INSERT OR IGNORE INTO types (id, name, icon) VALUES (?, ?, ?)", row
        )

    themes_seed = [
        (1,  "Python Général",  "🔄"),
        (2,  "FastAPI",         "⚡"),
        (3,  "Android",         "🤖"),
        (4,  "Jetpack Compose", "🎨"),
        (5,  "Kotlin",          "🔧"),
        (6,  "Réseau & API",    "🌐"),
        (7,  "Base de données", "💾"),
        (8,  "Tests",           "🧪"),
        (9,  "Dépendances",     "📦"),
        (10, "IDE",             "🛠️"),
        (11, "Architecture",    "📌"),
        (12, "Outils",          "📌"),
        (13, "IA & LLM",        "📌"),
    ]
    for row in themes_seed:
        cursor.execute(
            "INSERT OR IGNORE INTO themes (id, name, icon) VALUES (?, ?, ?)", row
        )

    conn.commit()
    conn.close()
