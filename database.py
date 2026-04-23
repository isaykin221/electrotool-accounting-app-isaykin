import sqlite3
from pathlib import Path


DB_PATH = Path(__file__).with_name("electrotools.db")


def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


def init_db():
    with get_connection() as connection:
        connection.executescript(
            """
            CREATE TABLE IF NOT EXISTS tools (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                inventory_number TEXT NOT NULL UNIQUE,
                name TEXT NOT NULL,
                category TEXT NOT NULL,
                location TEXT NOT NULL,
                responsible TEXT,
                condition TEXT NOT NULL DEFAULT 'исправен',
                status TEXT NOT NULL DEFAULT 'in_stock'
                    CHECK (status IN ('in_stock', 'issued', 'repair')),
                created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
            );

            CREATE TABLE IF NOT EXISTS issue_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_id INTEGER NOT NULL,
                employee TEXT NOT NULL,
                issued_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                planned_return_at TEXT,
                returned_at TEXT,
                FOREIGN KEY (tool_id) REFERENCES tools(id) ON DELETE CASCADE
            );

            CREATE TABLE IF NOT EXISTS maintenance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tool_id INTEGER NOT NULL,
                started_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                description TEXT NOT NULL,
                cost REAL NOT NULL DEFAULT 0,
                status TEXT NOT NULL DEFAULT 'open'
                    CHECK (status IN ('open', 'closed')),
                FOREIGN KEY (tool_id) REFERENCES tools(id) ON DELETE CASCADE
            );
            """
        )


def seed_demo_data():
    with get_connection() as connection:
        count = connection.execute("SELECT COUNT(*) FROM tools").fetchone()[0]
        if count:
            return

        connection.executemany(
            """
            INSERT INTO tools
                (inventory_number, name, category, location, responsible, condition, status)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """,
            [
                ("EL-001", "Аккумуляторная дрель Bosch", "дрель", "склад 1", "", "исправен", "in_stock"),
                ("EL-002", "Перфоратор Makita HR2470", "перфоратор", "цех 2", "Иванов И.И.", "исправен", "issued"),
                ("EL-003", "Мультиметр цифровой", "измерительный прибор", "лаборатория", "", "требует проверки", "repair"),
            ],
        )
        connection.execute(
            """
            INSERT INTO issue_history (tool_id, employee, planned_return_at)
            VALUES (
                (SELECT id FROM tools WHERE inventory_number = 'EL-002'),
                'Иванов И.И.',
                '2026-04-30'
            )
            """
        )
        connection.execute(
            """
            INSERT INTO maintenance (tool_id, description, cost, status)
            VALUES (
                (SELECT id FROM tools WHERE inventory_number = 'EL-003'),
                'Проверка щупов и калибровка прибора',
                1200,
                'open'
            )
            """
        )


def get_tools(status=None, search=None):
    query = "SELECT * FROM tools"
    conditions = []
    params = []

    if status:
        conditions.append("status = ?")
        params.append(status)

    if search:
        conditions.append(
            """
            (
                name LIKE ?
                OR inventory_number LIKE ?
                OR category LIKE ?
                OR location LIKE ?
                OR responsible LIKE ?
            )
            """
        )
        value = f"%{search}%"
        params.extend([value, value, value, value, value])

    if conditions:
        query += " WHERE " + " AND ".join(conditions)

    query += " ORDER BY created_at DESC, id DESC"

    with get_connection() as connection:
        rows = connection.execute(query, params).fetchall()
        return [dict(row) for row in rows]


def add_tool(inventory_number, name, category, location, condition):
    with get_connection() as connection:
        cursor = connection.execute(
            """
            INSERT INTO tools
                (inventory_number, name, category, location, condition)
            VALUES (?, ?, ?, ?, ?)
            """,
            (inventory_number, name, category, location, condition),
        )
        return cursor.lastrowid


def issue_tool(tool_id, employee, planned_return_at):
    with get_connection() as connection:
        tool = connection.execute(
            "SELECT status FROM tools WHERE id = ?",
            (tool_id,),
        ).fetchone()
        if not tool or tool["status"] != "in_stock":
            return False

        connection.execute(
            """
            UPDATE tools
            SET status = 'issued', responsible = ?
            WHERE id = ?
            """,
            (employee, tool_id),
        )
        connection.execute(
            """
            INSERT INTO issue_history (tool_id, employee, planned_return_at)
            VALUES (?, ?, ?)
            """,
            (tool_id, employee, planned_return_at),
        )
        return True


def return_tool(tool_id):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE tools
            SET status = 'in_stock', responsible = ''
            WHERE id = ?
            """,
            (tool_id,),
        )
        connection.execute(
            """
            UPDATE issue_history
            SET returned_at = CURRENT_TIMESTAMP
            WHERE id = (
                SELECT id
                FROM issue_history
                WHERE tool_id = ? AND returned_at IS NULL
                ORDER BY issued_at DESC
                LIMIT 1
            )
            """,
            (tool_id,),
        )


def send_to_repair(tool_id, description, cost=0):
    with get_connection() as connection:
        connection.execute(
            """
            UPDATE tools
            SET status = 'repair', responsible = '', condition = 'требует ремонта'
            WHERE id = ?
            """,
            (tool_id,),
        )
        connection.execute(
            """
            INSERT INTO maintenance (tool_id, description, cost)
            VALUES (?, ?, ?)
            """,
            (tool_id, description, cost),
        )


def get_maintenance():
    with get_connection() as connection:
        rows = connection.execute(
            """
            SELECT
                maintenance.id,
                maintenance.started_at,
                maintenance.description,
                maintenance.cost,
                maintenance.status,
                tools.inventory_number,
                tools.name
            FROM maintenance
            JOIN tools ON tools.id = maintenance.tool_id
            ORDER BY maintenance.started_at DESC
            """
        ).fetchall()
        return [dict(row) for row in rows]


def get_stats():
    with get_connection() as connection:
        rows = connection.execute(
            "SELECT status, COUNT(*) AS count FROM tools GROUP BY status"
        ).fetchall()
        stats = {"total": 0, "in_stock": 0, "issued": 0, "repair": 0}
        for row in rows:
            stats[row["status"]] = row["count"]
            stats["total"] += row["count"]
        return stats
