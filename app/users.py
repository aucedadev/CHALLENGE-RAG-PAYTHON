import sqlite3
from pathlib import Path
from typing import Optional

import bcrypt

from app.config import DATA_DIR


USERS_DB_PATH = DATA_DIR / "users.db"


def get_connection() -> sqlite3.Connection:
    connection = sqlite3.connect(USERS_DB_PATH)
    connection.row_factory = sqlite3.Row
    return connection


def initialize_users_db() -> None:
    USERS_DB_PATH.parent.mkdir(parents=True, exist_ok=True)

    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL CHECK(role IN ('admin', 'user')),
                is_active INTEGER NOT NULL DEFAULT 1,
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            )
            """
        )
        connection.commit()


def create_user(username: str, password: str, role: str = "user") -> bool:
    username = username.strip().lower()

    if not username or not password:
        raise ValueError("El usuario y la contraseña son obligatorios.")

    if role not in {"admin", "user"}:
        raise ValueError("El rol debe ser 'admin' o 'user'.")

    password_hash = bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(),
    ).decode("utf-8")

    try:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO users (username, password_hash, role)
                VALUES (?, ?, ?)
                """,
                (username, password_hash, role),
            )
            connection.commit()

        return True

    except sqlite3.IntegrityError:
        return False


def authenticate_user(username: str, password: str) -> Optional[dict]:
    username = username.strip().lower()

    with get_connection() as connection:
        user = connection.execute(
            """
            SELECT id, username, password_hash, role, is_active
            FROM users
            WHERE username = ?
            """,
            (username,),
        ).fetchone()

    if user is None or not user["is_active"]:
        return None

    password_is_valid = bcrypt.checkpw(
        password.encode("utf-8"),
        user["password_hash"].encode("utf-8"),
    )

    if not password_is_valid:
        return None

    return {
        "id": user["id"],
        "username": user["username"],
        "role": user["role"],
    }


def list_users() -> list[dict]:
    with get_connection() as connection:
        users = connection.execute(
            """
            SELECT id, username, role, is_active, created_at
            FROM users
            ORDER BY username
            """
        ).fetchall()

    return [dict(user) for user in users]


def set_user_active(user_id: int, is_active: bool) -> None:
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE users
            SET is_active = ?
            WHERE id = ?
            """,
            (int(is_active), user_id),
        )
        connection.commit()