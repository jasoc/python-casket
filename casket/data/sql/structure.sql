CREATE TABLE accounts (
  id_account INTEGER PRIMARY KEY AUTOINCREMENT,
  name       TEXT NOT NULL,
  password   TEXT NOT NULL,
  email      TEXT NOT NULL,
  other_json TEXT NOT NULL,
  id_session TEXT NOT NULL REFERENCES sessions(username)
);

CREATE TABLE sessions (
  username   TEXT PRIMARY KEY,
  email      TEXT NOT NULL
);
