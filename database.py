
import sqlite3
from typing import Optional, Dict, Any

class Database:
    def __init__(self, path: str = "bot.db"):
        self.path = path
        self._ensure()

    def _ensure(self):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    username TEXT,
                    language TEXT DEFAULT 'en',
                    role TEXT DEFAULT 'USER',
                    balance REAL DEFAULT 0,
                    status TEXT DEFAULT 'None',
                    config_seen INTEGER DEFAULT 0,
                    registered_at TEXT DEFAULT CURRENT_TIMESTAMP
                )
                """
            )
            cur.execute("PRAGMA table_info(users)")
            cols = [c[1] for c in cur.fetchall()]
            if "role" not in cols:
                cur.execute("ALTER TABLE users ADD COLUMN role TEXT DEFAULT 'USER'")
            if "balance" not in cols:
                cur.execute("ALTER TABLE users ADD COLUMN balance REAL DEFAULT 0")
            if "status" not in cols:
                cur.execute(
                    "ALTER TABLE users ADD COLUMN status TEXT DEFAULT 'None'"
                )
            if "config_seen" not in cols:
                cur.execute(
                    "ALTER TABLE users ADD COLUMN config_seen INTEGER DEFAULT 0"
                )
            if "setup_done" not in cols:
                cur.execute(
                    "ALTER TABLE users ADD COLUMN setup_done INTEGER DEFAULT 0"
                )
            if "registered_at" not in cols:
                cur.execute(
                    "ALTER TABLE users ADD COLUMN registered_at TEXT DEFAULT CURRENT_TIMESTAMP"
                )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS admin_status (
                    id INTEGER PRIMARY KEY CHECK (id=1),
                    is_online INTEGER DEFAULT 0
                )
                """
            )
            cur.execute(
                "INSERT OR IGNORE INTO admin_status (id, is_online) VALUES (1, 0)"
            )
            if "assigned_bot" not in cols:
                cur.execute("ALTER TABLE users ADD COLUMN assigned_bot TEXT")
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS user_features (
                    user_id INTEGER,
                    feature_key TEXT,
                    is_enabled INTEGER DEFAULT 0,
                    PRIMARY KEY (user_id, feature_key)
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS rdp_configs (
                    user_id INTEGER PRIMARY KEY,
                    email TEXT,
                    password TEXT,
                    ip TEXT,
                    name TEXT,
                    rdp_password TEXT,
                    expiry TEXT
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS subscriptions (
                    user_id INTEGER PRIMARY KEY,
                    package TEXT,
                    plan_type TEXT,
                    started_at TEXT DEFAULT CURRENT_TIMESTAMP,
                    expires_at TEXT,
                    reminder_sent INTEGER DEFAULT 0
                )
                """
            )
            cur.execute(
                """
                CREATE TABLE IF NOT EXISTS user_services (
                    user_id INTEGER,
                    service_key TEXT,
                    status TEXT,
                    expires_at TEXT,
                    PRIMARY KEY (user_id, service_key)
                )
                """
            )
            con.commit()

    def upsert_user(self, user_id: int, username: Optional[str], language: Optional[str] = None):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            # Try insert
            cur.execute(
                "INSERT OR IGNORE INTO users (user_id, username, language) VALUES (?, ?, ?)",
                (user_id, username, language or "en"),
            )
            # Update username and language if provided
            if username is not None:
                cur.execute("UPDATE users SET username=? WHERE user_id=?", (username, user_id))
            if language is not None:
                cur.execute("UPDATE users SET language=? WHERE user_id=?", (language, user_id))
            con.commit()

    def get_language(self, user_id: int) -> str:
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("SELECT language FROM users WHERE user_id=?", (user_id,))
            row = cur.fetchone()
            return row[0] if row and row[0] else "en"

    def get_user(self, user_id: int):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                "SELECT user_id, username, language, role, balance, status, config_seen, registered_at, assigned_bot FROM users WHERE user_id=?",
                (user_id,),
            )
            return cur.fetchone()

    def get_user_by_username(self, username: str):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                "SELECT user_id, username, language, role, balance, status, config_seen, registered_at, assigned_bot FROM users WHERE LOWER(username)=LOWER(?)",
                (username,),
            )
            return cur.fetchone()

    def get_balance(self, user_id: int) -> float:
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
            row = cur.fetchone()
            return row[0] if row else 0

    def get_status(self, user_id: int) -> str:
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("SELECT status FROM users WHERE user_id=?", (user_id,))
            row = cur.fetchone()
            return row[0] if row and row[0] else "None"

    def get_role(self, user_id: int) -> str:
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("SELECT role FROM users WHERE user_id=?", (user_id,))
            row = cur.fetchone()
            return row[0] if row and row[0] else "USER"

    def set_role(self, user_id: int, role: str):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("UPDATE users SET role=? WHERE user_id=?", (role, user_id))
            con.commit()

    def get_assigned_bot(self, user_id: int) -> Optional[str]:
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("SELECT assigned_bot FROM users WHERE user_id=?", (user_id,))
            row = cur.fetchone()
            if not row:
                return None
            value = row[0] or None
            if value:
                return value.lstrip("@")
            return None

    def set_assigned_bot(self, user_id: int, bot_username: Optional[str]):
        sanitized = bot_username.lstrip("@") if bot_username else None
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE users SET assigned_bot=? WHERE user_id=?",
                (sanitized, user_id),
            )
            con.commit()

    def set_balance(self, user_id: int, amount: float):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("UPDATE users SET balance=? WHERE user_id=?", (amount, user_id))
            con.commit()

    def set_status(self, user_id: int, status: str):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("UPDATE users SET status=? WHERE user_id=?", (status, user_id))
            con.commit()

    def get_setup_done(self, user_id: int) -> bool:
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("SELECT setup_done FROM users WHERE user_id=?", (user_id,))
            row = cur.fetchone()
            return bool(row[0]) if row else False

    def set_setup_done(self, user_id: int, done: bool):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE users SET setup_done=? WHERE user_id=?",
                (1 if done else 0, user_id),
            )
            con.commit()

    def get_config_seen(self, user_id: int) -> bool:
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("SELECT config_seen FROM users WHERE user_id=?", (user_id,))
            row = cur.fetchone()
            return bool(row[0]) if row else False

    def set_config_seen(self, user_id: int, seen: bool):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE users SET config_seen=? WHERE user_id=?",
                (1 if seen else 0, user_id),
            )
            con.commit()

    def add_balance(self, user_id: int, amount: float):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE users SET balance = balance + ? WHERE user_id=?",
                (amount, user_id),
            )
            con.commit()

    def deduct_balance(self, user_id: int, amount: float) -> bool:
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("SELECT balance FROM users WHERE user_id=?", (user_id,))
            row = cur.fetchone()
            if not row or row[0] < amount:
                return False
            new_balance = row[0] - amount
            cur.execute(
                "UPDATE users SET balance=? WHERE user_id=?",
                (new_balance, user_id),
            )
            con.commit()
            return True

    def get_user_feature_states(self, user_id: int):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                "SELECT feature_key, is_enabled FROM user_features WHERE user_id=?",
                (user_id,),
            )
            rows = cur.fetchall()
            return {key: bool(enabled) for key, enabled in rows}

    def set_user_feature_state(self, user_id: int, feature_key: str, enabled: bool):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                "INSERT INTO user_features (user_id, feature_key, is_enabled) VALUES (?, ?, ?)"
                " ON CONFLICT(user_id, feature_key) DO UPDATE SET is_enabled=excluded.is_enabled",
                (user_id, feature_key, 1 if enabled else 0),
            )
            con.commit()

    def get_admin_online(self) -> bool:
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("SELECT is_online FROM admin_status WHERE id=1")
            row = cur.fetchone()
            return bool(row[0]) if row else False

    def set_admin_online(self, online: bool):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE admin_status SET is_online=? WHERE id=1",
                (1 if online else 0,),
            )
            con.commit()

    def set_subscription(
        self,
        user_id: int,
        package: str,
        plan_type: str,
        expires_at: Optional[str],
    ):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                """
                INSERT INTO subscriptions (user_id, package, plan_type, expires_at, reminder_sent)
                VALUES (?, ?, ?, ?, 0)
                ON CONFLICT(user_id) DO UPDATE SET
                    package=excluded.package,
                    plan_type=excluded.plan_type,
                    expires_at=excluded.expires_at,
                    reminder_sent=0,
                    started_at=CURRENT_TIMESTAMP
                """,
                (user_id, package, plan_type, expires_at),
            )
            con.commit()

    def get_subscription(self, user_id: int) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.path) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(
                "SELECT package, plan_type, started_at, expires_at, reminder_sent FROM subscriptions WHERE user_id=?",
                (user_id,),
            )
            row = cur.fetchone()
            if not row:
                return None
            return {
                "package": row["package"],
                "plan_type": row["plan_type"],
                "started_at": row["started_at"],
                "expires_at": row["expires_at"],
                "reminder_sent": bool(row["reminder_sent"]),
            }

    def set_subscription_reminder(self, user_id: int, sent: bool):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                "UPDATE subscriptions SET reminder_sent=? WHERE user_id=?",
                (1 if sent else 0, user_id),
            )
            con.commit()

    def set_service(
        self,
        user_id: int,
        service_key: str,
        status: str,
        expires_at: Optional[str] = None,
    ):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                """
                INSERT INTO user_services (user_id, service_key, status, expires_at)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(user_id, service_key) DO UPDATE SET
                    status=excluded.status,
                    expires_at=excluded.expires_at
                """,
                (user_id, service_key, status, expires_at),
            )
            con.commit()

    def get_service(self, user_id: int, service_key: str) -> Optional[Dict[str, Any]]:
        with sqlite3.connect(self.path) as con:
            con.row_factory = sqlite3.Row
            cur = con.cursor()
            cur.execute(
                "SELECT status, expires_at FROM user_services WHERE user_id=? AND service_key=?",
                (user_id, service_key),
            )
            row = cur.fetchone()
            if not row:
                return None
            return {"status": row["status"], "expires_at": row["expires_at"]}

    def set_rdp_config(
        self,
        user_id: int,
        email: str,
        password: str,
        ip: str,
        name: str,
        rdp_password: str,
        expiry: str,
    ):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                """
                REPLACE INTO rdp_configs
                (user_id, email, password, ip, name, rdp_password, expiry)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (user_id, email, password, ip, name, rdp_password, expiry),
            )
            con.commit()

    def get_rdp_config(self, user_id: int):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute(
                "SELECT email, password, ip, name, rdp_password, expiry FROM rdp_configs WHERE user_id=?",
                (user_id,),
            )
            row = cur.fetchone()
            if row:
                return {
                    "email": row[0],
                    "password": row[1],
                    "ip": row[2],
                    "name": row[3],
                    "rdp_password": row[4],
                    "expiry": row[5],
                }
            return None

    def get_setup_users(self):
        with sqlite3.connect(self.path) as con:
            cur = con.cursor()
            cur.execute("SELECT user_id, username FROM users WHERE setup_done=1")
            return cur.fetchall()

