-- Schema for a lapsed-client recovery CRM

CREATE TABLE IF NOT EXISTS client_database (
    client_id       TEXT PRIMARY KEY,
    spend_gbp       NUMERIC(10,2),
    visits          INTEGER,
    first_visit     DATE,
    last_visit      DATE,
    contact_result  TEXT,
    comment         TEXT
);

CREATE TABLE IF NOT EXISTS recovery_action_log (
    id              INTEGER PRIMARY KEY AUTOINCREMENT,
    client_id       TEXT NOT NULL REFERENCES client_database(client_id),
    spend_gbp       NUMERIC(10,2),
    last_visit      DATE,
    contact_date    DATE,
    method          TEXT,
    result          TEXT,
    followup_date   DATE,
    notes           TEXT
);

CREATE INDEX IF NOT EXISTS idx_client_visits ON client_database(visits);
CREATE INDEX IF NOT EXISTS idx_action_client ON recovery_action_log(client_id);
