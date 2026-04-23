PRAGMA foreign_keys = ON;

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
