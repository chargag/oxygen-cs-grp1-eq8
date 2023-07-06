CREATE SCHEMA oxygencs;

CREATE TABLE oxygencs.event_log (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    created_at TEXT NOT NULL,
    event TEXT NOT NULL
);
