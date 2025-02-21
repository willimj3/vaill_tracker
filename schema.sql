DROP TABLE IF EXISTS state_legislation;

CREATE TABLE state_legislation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    state TEXT NOT NULL,
    bill_number TEXT NOT NULL,
    scope TEXT,
    key_provisions TEXT,
    summary TEXT,
    status TEXT NOT NULL
);
