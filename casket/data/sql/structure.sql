CREATE TABLE IF NOT EXISTS accounts (
  id_account INTEGER PRIMARY KEY AUTOINCREMENT,
  name       TEXT NOT NULL,
  password   TEXT NOT NULL,
  attributes TEXT NOT NULL,
  algorithm  TEXT NOT NULL,
  id_session TEXT NOT NULL REFERENCES sessions(username)
);

CREATE TABLE IF NOT EXISTS sessions (
  username   TEXT PRIMARY KEY,
  algorithm  TEXT NOT NULL
);
